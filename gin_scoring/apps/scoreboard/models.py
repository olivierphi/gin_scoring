import datetime as dt
import enum
from functools import cached_property
from typing import Literal, NamedTuple

from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _

from gin_scoring.lib.gin_rummy.consts import GameOutcome
from gin_scoring.lib.gin_rummy.rules import calculate_round_score


@enum.unique
class GameResultOutcome(models.IntegerChoices):
    DRAW = (0, _("Draw"))
    KNOCK = (1, _("Knock"))
    UNDERCUT = (2, _("Undercut"))
    GIN = (3, _("Gin"))
    BIG_GIN = (4, _("Big Gin"))


@enum.unique
class PlayerRef(models.IntegerChoices):
    PLAYER_1 = (1, _("Player 1"))  # the "player_1" of its PlayerPair
    PLAYER_2 = (2, _("Player 2"))  # the "player_2" of its PlayerPair


GAME_OUTCOMES_MAPPING: dict[GameResultOutcome, GameOutcome] = {
    # A mapping between our Django enum and the "domain" one:
    GameResultOutcome.DRAW: GameOutcome.DRAW,
    GameResultOutcome.KNOCK: GameOutcome.KNOCK,
    GameResultOutcome.UNDERCUT: GameOutcome.UNDERCUT,
    GameResultOutcome.GIN: GameOutcome.GIN,
    GameResultOutcome.BIG_GIN: GameOutcome.BIG_GIN,
}


class Player(NamedTuple):
    id: Literal[1, 2]
    name: str
    color: str  # A hex color code


class PlayerPair(models.Model):
    COLOR_PALETTE = [
        (
            "#FF6600",
            "orange",
        ),
        (
            "#336699",
            "blue",
        ),
    ]

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    player_1_name = models.CharField(max_length=50)
    player_2_name = models.CharField(max_length=50)
    player_1_color = ColorField(samples=COLOR_PALETTE, default="#FF6600")
    player_2_color = ColorField(samples=COLOR_PALETTE, default="#336699")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.player_1_name} & {self.player_2_name}"

    @cached_property
    def players(self) -> tuple[Player, Player]:
        return Player(1, self.player_1_name, self.player_1_color), Player(
            2, self.player_2_name, self.player_2_color
        )

    def get_player_by_ref(self, player_ref: PlayerRef) -> Player:
        return self.players[0] if player_ref == PlayerRef.PLAYER_1 else self.players[1]


class GameResultManager(models.Manager):

    @staticmethod
    def get_player_pair_last_game_results(
        player_pair: PlayerPair,
    ) -> "models.QuerySet[GameResult]":
        return GameResult.objects.filter(player_pair=player_pair).order_by(
            "-created_at"
        )[:10]

    @staticmethod
    def get_player_pair_hall_of_fame(
        player_pair: PlayerPair,
    ) -> "tuple[HallOfFameResult, HallOfFameResult]":
        """
        The overall "hall of fame" for a player pair, from their very 1st game.
        The winning player comes first in the tuple.
        """
        from .business_logic._get_player_pair_hall_of_fame import (
            get_player_pair_hall_of_fame,
        )

        return get_player_pair_hall_of_fame(player_pair)

    @staticmethod
    def get_player_pair_hall_of_fame_monthly(
        player_pair: PlayerPair,
    ) -> "list[HallOfFameMonthResult]":
        from .business_logic._get_player_pair_hall_of_fame_monthly import (
            get_player_pair_hall_of_fame_monthly,
        )

        return get_player_pair_hall_of_fame_monthly(player_pair)


class GameResult(models.Model):
    player_pair = models.ForeignKey(PlayerPair, on_delete=models.CASCADE)

    outcome = models.PositiveSmallIntegerField(choices=GameResultOutcome)
    # These 2 ones can be `null` when the outcome is `draw`:
    winner = models.PositiveSmallIntegerField(choices=PlayerRef, null=True)
    deadwood = models.PositiveSmallIntegerField(null=True)
    # Computed from the previous `outcome` and `deadwood` fields:
    winner_score = models.PositiveSmallIntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GameResultManager()

    def save(self, **kwargs) -> None:  # type: ignore[override]
        # The `winner_score` field should always be based on the `outcome` and
        # `deadwood` fields, rather than set externally:
        self._set_winner_score_from_outcome_and_deadwood()

        return super().save(**kwargs)

    @property
    def is_draw(self) -> bool:
        return self.outcome == GameResultOutcome.DRAW

    @cached_property
    def winner_name(self) -> str | None:
        """⚠️ Triggers a database call if the `player_pair` is not attached yet"""
        if self.winner is None:
            return None
        return (
            self.player_1_name
            if self.winner == PlayerRef.PLAYER_1
            else self.player_2_name
        )

    @cached_property
    def player_1_name(self) -> str:
        """⚠️ Triggers a database call if the `player_pair` is not attached yet"""
        return self.player_pair.player_1_name

    @cached_property
    def player_2_name(self) -> str:
        """⚠️ Triggers a database call if the `player_pair` is not attached yet"""
        return self.player_pair.player_2_name

    def __str__(self) -> str:
        return f"{self.player_1_name.title()} vs {self.player_2_name.title()}, on {self.created_at.strftime('%a %d %b at %H:%M')}"

    def _set_winner_score_from_outcome_and_deadwood(self) -> None:
        assert isinstance(self.outcome, GameResultOutcome)
        assert self.deadwood is not None

        if self.outcome is GameResultOutcome.DRAW:
            self.winner = None
            self.deadwood = 0
            self.winner_score = 0
        else:
            game_outcome_domain = GAME_OUTCOMES_MAPPING[self.outcome]
            self.winner_score = calculate_round_score(
                game_outcome=game_outcome_domain, deadwood=self.deadwood
            )


class HallOfFameResult(NamedTuple):
    player: Player
    wins_count: int
    wins_percentage: int
    total_score: int
    grand_total: int
    total_score_delta: int | None
    grand_total_delta: int | None


class HallOfFameMonthResult(NamedTuple):
    month: dt.date
    winner: Player
    winner_total_score: int
    winner_grand_total: int
    game_counts: int
    wins_count: int
    wins_percentage: int
    total_score_delta: int | None
    grand_total_delta: int | None


class CurrentMonthResult(NamedTuple):
    player: Player
    wins_count: int
    wins_percentage: int
    total_score: int
    grand_total: int
    total_score_delta: int | None
    grand_total_delta: int | None


def create_current_month_results_from_current_month_hall_of_fame(
    *, player_pair: PlayerPair, current_month_hall_of_fame: HallOfFameMonthResult
) -> tuple[CurrentMonthResult, CurrentMonthResult]:
    cur_month = current_month_hall_of_fame  # let's shorten that a bit internally 😅
    winner = cur_month.winner
    winner_result = CurrentMonthResult(
        player=winner,
        wins_count=cur_month.wins_count,
        wins_percentage=cur_month.wins_percentage,
        total_score=cur_month.winner_total_score,
        grand_total=cur_month.winner_grand_total,
        total_score_delta=None,
        grand_total_delta=None,
    )

    loser = (
        player_pair.players[1]
        if winner.id == PlayerRef.PLAYER_1
        else player_pair.players[0]
    )
    game_counts = cur_month.game_counts
    loser_wins_count = game_counts - winner_result.wins_count
    loser_total_score = winner_result.total_score - (cur_month.total_score_delta or 0)
    loser_grand_total = winner_result.grand_total - (cur_month.grand_total_delta or 0)
    loser_result = CurrentMonthResult(
        player=loser,
        wins_count=loser_wins_count,
        wins_percentage=100 - winner_result.wins_percentage,
        total_score=loser_total_score,
        grand_total=loser_grand_total,
        total_score_delta=-(cur_month.total_score_delta or 0),
        grand_total_delta=-(cur_month.grand_total_delta or 0),
    )

    return winner_result, loser_result
