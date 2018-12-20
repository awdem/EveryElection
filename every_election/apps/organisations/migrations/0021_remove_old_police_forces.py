# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-24 15:04
from __future__ import unicode_literals

from django.db import migrations

from organisations import constants


class Migration(migrations.Migration):

    dependencies = [("organisations", "0020_rename_police_force_to_area")]

    def remove_old_areas(apps, schema_editor):
        Organisation = apps.get_model("organisations", "Organisation")

        Organisation.objects.filter(
            organisation_type="police_area", slug__in=constants.AREAS_WITHOUT_PCCS
        ).delete()

    def do_nothing(apps, schema_editor):
        pass

    operations = [migrations.RunPython(remove_old_areas, do_nothing)]
