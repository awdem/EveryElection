from django.core.management import BaseCommand
from organisations.boundaries.boundary_bot.scraper import LgbceScraper


class Command(BaseCommand):
    help = "Scrape LGBCE website for boundary reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--bootstrap",
            action="store_true",
            help="Indicates command is running for the first time",
        )

    def handle(self, *args, **options):
        bootstrap_mode = options["bootstrap"]
        send_notifications = not (bootstrap_mode)
        scraper = LgbceScraper(bootstrap_mode, send_notifications)
        scraper.scrape()
