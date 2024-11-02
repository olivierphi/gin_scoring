# Generated by Django 5.1.1 on 2024-11-02 18:25

import colorfield.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerPair",
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
                ("player_1_name", models.CharField(max_length=50)),
                ("player_2_name", models.CharField(max_length=50)),
                (
                    "player_1_color",
                    colorfield.fields.ColorField(
                        default="#FF6600",
                        image_field=None,
                        max_length=25,
                        samples=[("#FF6600", "orange"), ("#336699", "blue")],
                    ),
                ),
                (
                    "player_2_color",
                    colorfield.fields.ColorField(
                        default="#336699",
                        image_field=None,
                        max_length=25,
                        samples=[("#FF6600", "orange"), ("#336699", "blue")],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GameResult",
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
                    "outcome",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Draw"),
                            (1, "Knock"),
                            (2, "Undercut"),
                            (3, "Gin"),
                            (4, "Big Gin"),
                        ]
                    ),
                ),
                (
                    "winner",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Player 1"), (2, "Player 2")], null=True
                    ),
                ),
                ("deadwood_value", models.PositiveSmallIntegerField(null=True)),
                ("winner_score", models.PositiveSmallIntegerField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "player_pair",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scoreboard.playerpair",
                    ),
                ),
            ],
        ),
    ]