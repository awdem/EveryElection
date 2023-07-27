from django.test import TestCase
from organisations.tests.factories import (
    DivisionGeographyFactory,
    OrganisationDivisionFactory,
    OrganisationDivisionSetFactory,
    OrganisationFactory,
)


class TestElectionIDs(TestCase):
    def test_organisation_factory(self):
        o = OrganisationFactory()
        assert o.slug == "org-{}".format(o.official_identifier)

    def test_organisation_division_set_factory(self):
        ods = OrganisationDivisionSetFactory()
        assert ods.organisation.slug.startswith("org-")

    def test_organisation_division_factory(self):
        od = OrganisationDivisionFactory()
        assert od.organisation.slug.startswith("org-")

    def test_division_geography_factory(self):
        DivisionGeographyFactory()
