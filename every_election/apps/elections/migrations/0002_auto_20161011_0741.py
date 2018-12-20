# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 07:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("elections", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="ElectionSubType",
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
                ("name", models.CharField(blank=True, max_length=100)),
                ("election_subtype", models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.RemoveField(model_name="electiontype", name="election_subtype"),
        migrations.AddField(
            model_name="electionsubtype",
            name="election_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subtype",
                to="elections.ElectionType",
            ),
        ),
    ]
