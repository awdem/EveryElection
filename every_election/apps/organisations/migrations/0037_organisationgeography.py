# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-07 09:02
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0036_auto_20180606_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationGeography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('gss', models.CharField(blank=True, max_length=20)),
                ('legislation_url', models.CharField(blank=True, max_length=500, null=True)),
                ('geography', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='geographies', to='organisations.Organisation')),
            ],
        ),
    ]
