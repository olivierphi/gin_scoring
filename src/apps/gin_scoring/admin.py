from django.contrib import admin

from .models import GameResult


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "player_north_name",
        "player_south_name",
        "outcome",
        "winner_name",
        "winner_score",
    )
    list_filter = ("outcome", "winner_name")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
