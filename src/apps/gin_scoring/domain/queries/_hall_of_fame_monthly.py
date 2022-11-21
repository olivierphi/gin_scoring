from collections import defaultdict
from datetime import datetime
from typing import NamedTuple

from sqlalchemy import func, select, desc, Row

from db.session import db_session

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

    first_pass_cte = (
        select(
            GameResult.winner_name,
            GameResult.winner_score,
            func.date_trunc("month", GameResult.created_at).label("month"),
        )
        .where(GameResult.winner_name.is_not(None))
        .cte("monthly_stats_per_player_pass_1")
    )
    second_pass_cte = (
        select(
            first_pass_cte.c.winner_name,
            first_pass_cte.c.month,
            func.count(first_pass_cte.c.winner_score).label("win_counts"),
            func.sum(first_pass_cte.c.winner_score).label("total_score"),
        )
        .group_by(first_pass_cte.c.month, first_pass_cte.c.winner_name)
        .cte("monthly_stats_per_player_pass_2")
    )
    stmt = select(
        second_pass_cte.c.winner_name,
        second_pass_cte.c.month,
        second_pass_cte.c.win_counts,
        second_pass_cte.c.total_score,
        ((second_pass_cte.c.win_counts * 25) + second_pass_cte.c.total_score).label("grand_total"),
    ).order_by(desc("month"), desc("grand_total"))

    raw_results_per_month: dict[datetime, list[Row]] = defaultdict(list)
    for raw_result in db_session.execute(stmt).all():
        raw_results_per_month[raw_result.month].append(raw_result)

    returned_results: list[HallOfFameMonthResult] = []
    for month, month_results in raw_results_per_month.items():
        winner_result = month_results[0]
        winner_grand_total = winner_result.grand_total or 0
        second_best_grand_total = 0 if len(month_results) < 2 else (month_results[1].grand_total or 0)
        games_count = sum([res.win_counts for res in month_results])

        returned_results.append(
            HallOfFameMonthResult(
                month=month,
                winner_name=winner_result.winner_name,
                game_counts=games_count,
                win_counts=winner_result.win_counts,
                score_delta=winner_grand_total - second_best_grand_total,
            )
        )

    return returned_results
