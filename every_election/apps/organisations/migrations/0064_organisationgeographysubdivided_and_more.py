# Generated by Django 4.1.7 on 2023-03-28 14:32

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0063_alter_divisiongeography_geography"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrganisationGeographySubdivided",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "geography",
                    django.contrib.gis.db.models.fields.PolygonField(
                        db_index=True, srid=4326
                    ),
                ),
                (
                    "organisation_geography",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subdivided",
                        to="organisations.organisationgeography",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DivisionGeographySubdivided",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "geography",
                    django.contrib.gis.db.models.fields.PolygonField(
                        db_index=True, srid=4326
                    ),
                ),
                (
                    "division_geography",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subdivided",
                        to="organisations.divisiongeography",
                    ),
                ),
            ],
        ),
    ]
