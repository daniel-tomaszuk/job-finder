# Generated by Django 5.0.6 on 2024-05-20 11:21

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="KeyWord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key_word", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="ScrappingProcess",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Selector",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "selector_type",
                    models.CharField(
                        choices=[
                            ("element_id", "element_id"),
                            ("class_name", "class_name"),
                            ("partial_link_text", "partial_link_text"),
                            ("css_selector", "css_selector"),
                            ("selector_none", "selector_none"),
                        ],
                        max_length=32,
                    ),
                ),
                ("selector_value", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="Seniority",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("junior", "junior"),
                            ("mid", "mid"),
                            ("regular", "regular"),
                            ("senior", "senior"),
                            ("other", "other"),
                        ],
                        default="other",
                        max_length=16,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "seniorities",
            },
        ),
        migrations.CreateModel(
            name="ScrappingStep",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("is_input_step", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "key_words",
                    models.ManyToManyField(
                        related_name="scrapping_steps", to="scrapping_process.keyword"
                    ),
                ),
                (
                    "process",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="steps",
                        to="scrapping_process.scrappingprocess",
                    ),
                ),
                (
                    "selector",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scrapping_steps",
                        to="scrapping_process.selector",
                    ),
                ),
                (
                    "seniorities",
                    models.ManyToManyField(
                        related_name="scrapping_steps", to="scrapping_process.seniority"
                    ),
                ),
            ],
        ),
    ]