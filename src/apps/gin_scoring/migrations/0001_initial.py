# Generated by Django 4.0.5 on 2022-06-20 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GameResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("player_north_name", models.CharField(max_length=50)),
                ("player_south_name", models.CharField(max_length=50)),
                (
                    "outcome",
                    models.CharField(
                        choices=[
                            ("knock", "knock"),
                            ("gin", "gin"),
                            ("big_gin", "big_gin"),
                            ("undercut", "undercut"),
                            ("draw", "draw"),
                        ],
                        max_length=10,
                    ),
                ),
                ("winner_name", models.CharField(max_length=50, null=True)),
                ("deadwood_value", models.PositiveSmallIntegerField(null=True)),
                ("winner_score", models.PositiveSmallIntegerField(null=True)),
                ("created_at", models.DateTimeField(django.utils.timezone.now)),
            ],
        ),
    ]
