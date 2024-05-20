# Generated by Django 5.0.6 on 2024-05-20 12:24

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("scrapping_process", "0002_alter_scrappingstep_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="scrappingstep",
            name="many",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="scrappingstep",
            name="seniorities",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="scrapping_steps",
                to="scrapping_process.seniority",
            ),
        ),
    ]