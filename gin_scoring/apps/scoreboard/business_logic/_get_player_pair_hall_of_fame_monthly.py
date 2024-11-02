import datetime as dt
from collections import defaultdict
from typing import TYPE_CHECKING

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

from ..models import GameResult, HallOfFameMonthResult, PlayerRef

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..models import PlayerPair


def get_player_pair_hall_of_fame_monthly(
    player_pair: "PlayerPair",
) -> "Sequence[HallOfFameMonthResult]":
    # @link https://docs.djangoproject.com/en/5.1/topics/db/aggregation/
    wins_count = Count("winner_score")
    total_score = Sum("winner_score")

    raw_results = (
        GameResult.objects.filter(player_pair=player_pair)
        .filter(winner__isnull=False)
        .annotate(month=TruncMonth("created_at"))
        .values("month", "winner")
        .distinct()
        .annotate(wins_count=wins_count, total_score=total_score)
        # Each won round is worth 25 points:
        .annotate(grand_total=(wins_count * 25) + total_score)
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
        games_count = sum([res["wins_count"] for res in month_results])

        returned_results.append(
            HallOfFameMonthResult(
                month=month,
                winner=player_pair.get_player_by_ref(winner_result["winner"]),
                game_counts=games_count,
                wins_count=winner_result["wins_count"],
                wins_percentage=(
                    int(winner_result["wins_count"] / games_count * 100)
                    if games_count
                    else 0
                ),
                score_delta=winner_grand_total - second_best_grand_total,
            )
        )

    return returned_results
