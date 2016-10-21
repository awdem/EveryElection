# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0007_auto_20161021_1609'),
        ('elections', '0004_electedrole'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('election_id', models.CharField(blank=True, max_length=100)),
                ('poll_open_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ElectionDivisions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_contested', models.IntegerField()),
                ('seats_total', models.IntegerField()),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.OrganisationDivision')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Election')),
            ],
        ),
        migrations.AddField(
            model_name='election',
            name='divisions',
            field=models.ManyToManyField(through='elections.ElectionDivisions', to='organisations.OrganisationDivision'),
        ),
        migrations.AddField(
            model_name='election',
            name='election_subtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elections.ElectionSubType'),
        ),
        migrations.AddField(
            model_name='election',
            name='election_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.ElectionType'),
        ),
        migrations.AddField(
            model_name='election',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.Organisation'),
        ),
    ]
