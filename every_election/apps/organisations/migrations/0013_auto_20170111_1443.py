# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-11 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("organisations", "0012_auto_20170111_1441")]

    operations = [
        migrations.AddField(
            model_name="organisationdivisionset",
            name="legislation_url",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="organisationdivisionset",
            name="notes",
            field=models.TextField(blank=True),
        ),
    ]
