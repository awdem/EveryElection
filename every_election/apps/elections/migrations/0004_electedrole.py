# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 18:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("organisations", "0004_auto_20161010_1802"),
        ("elections", "0003_initial_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="ElectedRole",
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
                ("elected_title", models.CharField(blank=True, max_length=255)),
                (
                    "election_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elections.ElectionType",
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organisations.Organisation",
                    ),
                ),
            ],
        )
    ]
