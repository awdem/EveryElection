# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-31 10:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("organisations", "0031_end_date_constraint")]

    operations = [
        migrations.AddField(
            model_name="organisation",
            name="end_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="organisation",
            name="start_date",
            field=models.DateField(default=datetime.date(2016, 10, 1)),
            preserve_default=False,
        ),
    ]
