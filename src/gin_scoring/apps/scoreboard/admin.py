from django.contrib import admin

from .models import GameResult, PlayerPair


@admin.register(PlayerPair)
class PlayerPairAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = (
        "player_pair",
        "created_at",
        "player_1_name",
        "player_2_name",
        "outcome",
        "winner_name",
        "winner_score",
    )
    list_filter = ("outcome", "player_pair")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
