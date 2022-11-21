from collections.abc import Iterator
from typing import NamedTuple

from sqlalchemy import func, select, desc

from db.session import db_session

# from django.db.models import Count, Sum

from ...models import GameResult


class HallOfFameResult(NamedTuple):
    winner_name: str
    win_counts: int
    total_score: int
    grand_total: int
    score_delta: int | None


def hall_of_fame() -> Iterator[HallOfFameResult]:
    # Let's aggregate some stats per player who won games first:
    first_pass_cte = (
        select(
            GameResult.winner_name,
            func.count(GameResult.winner_score).label("win_counts"),
            func.sum(GameResult.winner_score).label("total_score"),
        )
        .group_by(GameResult.winner_name)
        .distinct()
        .cte("stats_per_player_pass_1")
    )
    # ...and then, augment this with a "grand total":
    stmt = select(
        first_pass_cte.c.winner_name,
        first_pass_cte.c.win_counts,
        first_pass_cte.c.total_score,
        ((first_pass_cte.c.win_counts * 25) + first_pass_cte.c.total_score).label("grand_total"),
    ).order_by(desc("grand_total"))

    previous_score = 0
    for i, row in enumerate(db_session.execute(stmt).all()):
        score_delta = row.grand_total - previous_score if i > 0 else None
        yield HallOfFameResult(
            winner_name=row.winner_name,
            win_counts=row.win_counts,
            total_score=row.total_score,
            grand_total=row.grand_total,
            score_delta=score_delta,
        )
        previous_score = row.grand_total
