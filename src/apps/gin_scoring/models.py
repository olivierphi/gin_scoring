from functools import cached_property

from django.db import models

from .domain.gin_rummy import GAME_OUTCOME


class GameResult(models.Model):
    player_north_name = models.CharField(max_length=50)
    player_south_name = models.CharField(max_length=50)
    outcome = models.CharField(max_length=10, choices=[(end_type, end_type) for end_type in GAME_OUTCOME.__args__])  # type: ignore
    # These 2 ones can be `null` when the outcome is `draw`:
    winner_name = models.CharField(max_length=50, null=True)
    deadwood_value = models.PositiveSmallIntegerField(null=True)
    # Computed from the previous `end_type` and `deadwood_value` fields:
    winner_score = models.PositiveSmallIntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_draw(self) -> bool:
        return self.outcome == "draw"

    @cached_property
    def loser_name(self) -> str:
        return [name for name in (self.player_north_name, self.player_south_name) if name != self.winner_name][0]
