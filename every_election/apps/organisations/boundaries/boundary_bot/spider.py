import json
import tempfile

import scrapy
from organisations.boundaries.boundary_bot.common import (
    REQUEST_HEADERS,
    START_PAGE,
)
from organisations.boundaries.constants import LGBCE_SLUG_TO_ORG_SLUG
from organisations.models.divisions import ReviewStatus
from scrapy.crawler import CrawlerProcess


def get_link_from_container_label(label, response, link_div_class):
    """
    lgbce website has chunks of html like:

    <div class="link-name-and-view-container">
      <div class="link-name-container">
        <div class="link-title">The Mole Valley (Electoral Changes) Order 2023</div>
      </div>
      <div class="link-view-container">
        <a href="https://www.legislation.gov.uk/uksi/2023/49/contents/made" target="_blank" rel="nofollow noopener noreferrer">
          View
          <span class="sr-only">(opens in a new tab)</span>
        </a>
      </div>
    </div>

    This method grabs the links contained by the grandparent of the div containing text matching lower.
    Search is case insensitive.
    Caller needs to check that there's only one link.
    """
    x_path = (
        f'//div[@class="{link_div_class}"][contains(translate('
        "text(),"
        '"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), '
        f'"{label.lower()}")]/../..//a/@href'
    )
    return response.xpath(x_path).extract()


class LgbceSpider(scrapy.Spider):
    name = "reviews"
    custom_settings = {
        "CONCURRENT_REQUESTS": 5,  # keep the concurrent requests low
        "DOWNLOAD_DELAY": 0.25,  # throttle the crawl speed a bit
        "COOKIES_ENABLED": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "FEED_FORMAT": "json",
        "DEFAULT_REQUEST_HEADERS": REQUEST_HEADERS,
        # "HTTPCACHE_ENABLED": True,  # Uncomment for Dev
    }
    allowed_domains = ["lgbce.org.uk"]
    start_urls = [START_PAGE]

    def get_shapefiles(self, response):
        # find any zipfile links in divs that also have a header element containing the text 'Final'
        zipfiles = response.xpath(
            "/html/body//div[h4[contains(text(), 'Final')]]//a[contains(@href,'.zip')]/@href"
        ).extract()

        if len(zipfiles) == 1:
            # if we found exactly one link to a zipfile,
            # assume that's what we're looking for
            return zipfiles[0]

        return None

    def get_latest_event(self, response):
        latest_stage = response.css("div.stage-latest")
        if latest_stage:
            return (
                latest_stage.css("div > div > a > h3")
                .xpath("text()")[0]
                .extract()
                .strip()
            )
        return None

    def get_eco_title_and_link(self, response, latest_event):
        def get_link_title(selector):
            return selector.xpath(
                '*/div[@class="link-title"]//text()'
            ).extract_first()

        def get_link(selector):
            return selector.xpath("*/a/@href").extract_first()

        def is_relevant_review(title):
            return (
                "(electoral changes) order" in title.lower()
                or "(structural changes) order" in title.lower()
                or "greater london authority"  # edge case to handle https://www.lgbce.org.uk/all-reviews/greater-london-authority
                in title.lower()
            )

        links = [
            (get_link_title(selector), get_link(selector))
            for selector in response.xpath(
                '//div[@class="latest-information"]//div[@class="link-name-and-view-container"]'
            )
        ]

        made_ecos = [
            (title, link) for title, link in links if is_relevant_review(title)
        ]

        if latest_event == "Effective date" and len(made_ecos) == 1:
            # This catches draft links and made links.
            # Sometimes they put a draft link in where the made link should go.
            # So, if the change is 'effective', and we only have a draft link,
            # use it
            return made_ecos[0]

        made_ecos = [
            (title, link)
            for title, link in made_ecos
            if is_relevant_review(title) and "ukdsi" not in link
        ]

        if len(made_ecos) == 1:
            return made_ecos[0]

        return None, None

    def get_status(self, response):
        lgbce_status = response.css("div.status::text")
        if lgbce_status:
            lgbce_status = lgbce_status.extract_first().strip()
        match lgbce_status:
            case "Currently in review":
                return ReviewStatus.CURRENT
            case "Completed":
                return ReviewStatus.COMPLETED
            case _:
                return None

    def parse(self, response):
        status = self.get_status(response)
        if status:
            latest_event = self.get_latest_event(response)
            if (
                latest_event == "Initial consultation"
                and status == ReviewStatus.COMPLETED
            ):
                status = ReviewStatus.CURRENT
            legislation_title, legislation_url = self.get_eco_title_and_link(
                response, latest_event
            )
            lgbce_slug = response.url.split("/")[-1]
            try:
                slug = LGBCE_SLUG_TO_ORG_SLUG[lgbce_slug]
            except KeyError:
                slug = lgbce_slug
            rec = {
                "slug": slug,
                "latest_event": latest_event,
                "boundaries_url": self.get_shapefiles(response),
                "status": status,
                "legislation_url": legislation_url,
                "legislation_made": 0,
                "legislation_title": legislation_title,
            }

            if rec["legislation_url"]:
                rec["legislation_made"] = 1

            yield rec
        for next_page in response.css("div.letter_section > div > a"):
            if "all-reviews" in next_page.extract():
                yield response.follow(next_page, self.parse)


class SpiderWrapper:
    # Wrapper class that allows us to run a scrapy spider
    # and return the result as a list

    def __init__(self, spider):
        self.spider = spider

    def run_spider(self):
        # Scrapy likes to dump its output to file
        # so we will write it out to a file and read it back in.
        # The 'proper' way to do this is probably to write a custom Exporter
        # but this will do for now

        with tempfile.NamedTemporaryFile() as tmpfile:
            process = CrawlerProcess(
                {
                    "FEED_URI": tmpfile.name,
                }
            )
            process.crawl(self.spider)
            process.start()

            tmpfile.seek(0)
            return json.load(tmpfile)
