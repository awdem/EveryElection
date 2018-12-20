# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-07 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("elections", "0012_remove_ElectionDivisions")]

    operations = [
        migrations.AddField(
            model_name="election",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="elections.Election",
            ),
        )
    ]
