# Generated by Django 4.1.5 on 2023-01-25 10:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("elections", "0064_voting_system_to_charfield"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="electiontype",
            name="default_voting_system",
        ),
        migrations.DeleteModel(
            name="VotingSystem",
        ),
    ]