# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-01 14:37
from __future__ import unicode_literals

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("elections", "0044_auto_20181001_1114")]

    operations = [
        migrations.AlterModelManagers(
            name="election",
            managers=[("public_objects", django.db.models.manager.Manager())],
        )
    ]
