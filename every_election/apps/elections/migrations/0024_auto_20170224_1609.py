# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-24 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("elections", "0023_votingsystem_uses_party_lists")]

    operations = [
        migrations.AlterField(
            model_name="election",
            name="election_id",
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        )
    ]
