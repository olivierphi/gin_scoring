from collections import defaultdict
from datetime import datetime
from typing import NamedTuple

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

from ...models import GameResult


class HallOfFameMonthResult(NamedTuple):
    month: datetime
    winner_name: str
    game_counts: int
    win_counts: int
    score_delta: int


def hall_of_fame_monthly() -> list[HallOfFameMonthResult]:
    # ⚠️ Probably not the very best way to achieve this...
    # But this is a project I gave myself one single day to build,
    # so that will do the job 😅

    # @link https://docs.djangoproject.com/en/5.1/topics/db/aggregation/
    win_counts = Count("winner_score")
    total_score = Sum("winner_score")

    raw_results = (
        GameResult.objects.filter(winner_name__isnull=False)
        .annotate(month=TruncMonth("created_at"))
        .values("month", "winner_name")
        .distinct()
        .annotate(win_counts=win_counts, total_score=total_score)
        # Each won round is worth 25 points:
        .annotate(grand_total=(win_counts * 25) + total_score)
        .order_by("-month", "-grand_total")
    )
    raw_results_per_month: dict[datetime, list[dict]] = defaultdict(list)
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
