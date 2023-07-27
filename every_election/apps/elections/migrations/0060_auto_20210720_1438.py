# Generated by Django 2.2.20 on 2021-07-20 14:38

from django.db import migrations
from django.db.models import JSONField


class Migration(migrations.Migration):
    dependencies = [
        ("elections", "0059_election_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="election",
            name="tags",
            field=JSONField(blank=True, default=dict),
        ),
    ]
