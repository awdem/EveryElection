# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-25 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("elections", "0022_auto_20170125_1522")]

    operations = [
        migrations.AddField(
            model_name="votingsystem",
            name="uses_party_lists",
            field=models.BooleanField(default=False),
        )
    ]
