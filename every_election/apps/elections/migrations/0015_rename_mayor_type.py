# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 07:37
from __future__ import unicode_literals

from django.db import migrations


def rename_mayor_type(apps, schema_editor):
    ElectionType = apps.get_model("elections", "ElectionType")

    ElectionType.objects.filter(name="City mayor").update(name="Directly Elected Mayor")


def undo_rename_mayor_type(apps, schema_editor):
    ElectionType = apps.get_model("elections", "ElectionType")

    ElectionType.objects.filter(name="Directly Elected Mayor").update(name="City mayor")


class Migration(migrations.Migration):
    dependencies = [("elections", "0014_auto_20170107_1605")]

    operations = [migrations.RunPython(rename_mayor_type, undo_rename_mayor_type)]
