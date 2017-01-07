# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-07 11:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0010_election_elected_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='tmp_election_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='election',
            name='election_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='election',
            name='poll_open_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='election',
            name='poll_open_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='election',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.Organisation'),
        ),
    ]
