# Generated by Django 3.2 on 2022-03-07 05:59

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import easy_graphql_server.custom_json


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("female", "female"),
                            ("male", "male"),
                            ("other", "other"),
                        ],
                        default="other",
                        max_length=6,
                    ),
                ),
                ("username", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(blank=True, max_length=255)),
                ("first_name", models.CharField(max_length=32)),
                ("last_name", models.CharField(max_length=64)),
                ("birth_date", models.DateField(blank=True, null=True)),
                ("is_staff", models.BooleanField(blank=True, default=False)),
                ("is_superuser", models.BooleanField(blank=True, default=False)),
                ("updates_count", models.IntegerField(blank=True, default=0)),
                (
                    "creation_data",
                    models.JSONField(
                        blank=True,
                        encoder=easy_graphql_server.custom_json.JSONEncoder,
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "auth_user",
                "ordering": ("id",),
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="House",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("location", models.CharField(max_length=255)),
                ("construction_date", models.DateField(blank=True, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="houses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="DailyOccupation",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("hours_per_day", models.IntegerField()),
                (
                    "occupation",
                    models.CharField(
                        choices=[
                            ("EAT", "EAT"),
                            ("SLEEP", "SLEEP"),
                            ("WORK", "WORK"),
                            ("COMMUTE", "COMMUTE"),
                            ("_", "_"),
                        ],
                        max_length=7,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_occupations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="BankAccount",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("iban", models.CharField(max_length=34)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bank_accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.AddField(
            model_name="person",
            name="home",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tenants",
                to="django.house",
            ),
        ),
    ]
