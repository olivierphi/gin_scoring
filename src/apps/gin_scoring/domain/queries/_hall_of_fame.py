from collections.abc import Iterator
from typing import NamedTuple

from django.db.models import Count, Sum

from ...models import GameResult


class HallOfFameResult(NamedTuple):
    winner_name: str
    win_counts: int
    total_score: int
    grand_total: int
    score_delta: int | None


def hall_of_fame() -> Iterator[HallOfFameResult]:
    # @link https://docs.djangoproject.com/en/4.0/topics/db/aggregation/
    win_counts = Count("winner_score")
    total_score = Sum("winner_score")

    query_set = (
        GameResult.objects.filter(winner_name__isnull=False)
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
