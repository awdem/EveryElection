# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-03 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0050_remove_organisationdivision_geography_curie'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationdivision',
            name='temp_id',
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
    ]