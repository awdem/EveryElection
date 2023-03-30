# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-14 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("organisations", "0027_auto_20171208_1049")]

    operations = [
        migrations.AlterField(
            model_name="organisationdivisionset",
            name="start_date",
            field=models.DateField(),
        ),
        migrations.AlterUniqueTogether(
            name="organisationdivisionset",
            unique_together=set([("organisation", "start_date")]),
        ),
    ]
