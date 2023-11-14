# Generated by Django 4.2.6 on 2023-11-14 11:18
import contextlib

from django.db import migrations


def rename_city_of_london(apps, schema_editor):
    Organisation = apps.get_model("organisations", "Organisation")

    with contextlib.suppress(Organisation.DoesNotExist):
        city_of_london_alder = Organisation.objects.get(
            official_identifier="LND-alder"
        )
        city_of_london_alder.official_name = (
            "City of London Corporation (Alderman)"
        )
        city_of_london_alder.start_date = "1189-01-01"
        city_of_london_alder.save()

    with contextlib.suppress(Organisation.DoesNotExist):
        city_of_london_common = Organisation.objects.get(
            official_identifier="LND"
        )
        city_of_london_common.official_name = (
            "City of London Corporation (Common Council)"
        )
        city_of_london_common.start_date = "1189-01-01"
        city_of_london_common.save()


class Migration(migrations.Migration):
    dependencies = [
        ("organisations", "0064_organisationgeographysubdivided_and_more"),
    ]

    operations = [
        migrations.RunPython(rename_city_of_london, migrations.RunPython.noop)
    ]
