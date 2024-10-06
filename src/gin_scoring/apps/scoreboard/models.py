import datetime as dt
import enum
from collections import defaultdict
from functools import cached_property
from typing import TYPE_CHECKING, NamedTuple

from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence


@enum.unique
class GameResultOutcome(models.IntegerChoices):
    DRAW = (0, _("draw"))
    KNOCK = (1, _("knock"))
    UNDERCUT = (2, _("undercut"))
    GIN = (3, _("gin"))
    BIG_GIN = (4, _("big_gin"))


@enum.unique
class PlayerRef(models.IntegerChoices):
    PLAYER_1 = (1, _("Player 1"))  # the "player_1" of its PlayerPair
    PLAYER_2 = (2, _("Player 2"))  # the "player_2" of its PlayerPair


class PlayerPair(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    player_1_name = models.CharField(max_length=50)
    player_2_name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.player_1_name} & {self.player_2_name}"


class GameResultManager(models.Manager):
    def get_player_pair_last_game_results(
        self, player_pair: PlayerPair
    ) -> "models.QuerySet[GameResult]":
        return GameResult.objects.filter(player_pair=player_pair).order_by(
            "-created_at"
        )[:10]

    def get_player_pair_hall_of_fame(
        self, player_pair: PlayerPair
    ) -> "Iterator[HallOfFameResult]":
        """
        The overall "hall of fame" for a player pair, from their very 1st game.
        """
        # @link https://docs.djangoproject.com/en/5.1/topics/db/aggregation/
        win_counts = Count("winner_score")
        total_score = Sum("winner_score")

        query_set = (
            GameResult.objects.filter(player_pair=player_pair)
            .filter(winner_name__isnull=False, winner_score__isnull=False)
            .values("winner_name")
            .distinct()
            .annotate(win_counts=win_counts, total_score=total_score)
            # Each won round is worth 25 points:
            .annotate(grand_total=(win_counts * 25) + total_score)
            .order_by("-grand_total")
        )

        previous_score = 0
        for i, row in enumerate(query_set):
            score_delta = row["grand_total"] - previous_score if i > 0 else None
            yield HallOfFameResult(
                winner_name=row["winner_name"],
                win_counts=row["win_counts"],
                total_score=row["total_score"],
                grand_total=row["grand_total"],
                score_delta=score_delta,
            )
            previous_score = row["grand_total"]

    def get_player_pair_hall_of_fame_monthly(
        self, player_pair: PlayerPair
    ) -> "Sequence[HallOfFameMonthResult]":
        # @link https://docs.djangoproject.com/en/5.1/topics/db/aggregation/
        win_counts = Count("winner_score")
        total_score = Sum("winner_score")

        raw_results = (
            GameResult.objects.filter(player_pair=player_pair)
            .filter(winner_name__isnull=False)
            .annotate(month=TruncMonth("created_at"))
            .values("month", "winner_name")
            .distinct()
            .annotate(win_counts=win_counts, total_score=total_score)
            # Each won round is worth 25 points:
            .annotate(grand_total=(win_counts * 25) + total_score)
            .order_by("-month", "-grand_total")
        )
        raw_results_per_month: dict[dt.datetime, list[dict]] = defaultdict(list)
        for raw_result in raw_results:
            raw_results_per_month[raw_result["month"]].append(raw_result)

        returned_results: list[HallOfFameMonthResult] = []
        for month, month_results in raw_results_per_month.items():
            winner_result = month_results[0]
            winner_grand_total = winner_result["grand_total"] or 0
            second_best_grand_total = (
                0 if len(month_results) < 2 else (month_results[1]["grand_total"] or 0)
            )
            games_count = sum([res["win_counts"] for res in month_results])

            returned_results.append(
                HallOfFameMonthResult(
                    month=month,
                    winner_name=winner_result["winner_name"],
                    game_counts=games_count,
                    win_counts=winner_result["win_counts"],
                    score_delta=winner_grand_total - second_best_grand_total,
                )
            )

        return returned_results


class GameResult(models.Model):
    player_pair = models.ForeignKey(PlayerPair, on_delete=models.CASCADE)

    outcome = models.PositiveSmallIntegerField(choices=GameResultOutcome)
    # These 2 ones can be `null` when the outcome is `draw`:
    winner = models.PositiveSmallIntegerField(choices=PlayerRef, null=True)
    deadwood_value = models.PositiveSmallIntegerField(null=True)
    # Computed from the previous `end_type` and `deadwood_value` fields:
    winner_score = models.PositiveSmallIntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GameResultManager

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


class HallOfFameResult(NamedTuple):
    winner_name: str
    win_counts: int
    total_score: int
    grand_total: int
    score_delta: int | None


class HallOfFameMonthResult(NamedTuple):
    month: dt.datetime
    winner_name: str
    game_counts: int
    win_counts: int
    score_delta: int
