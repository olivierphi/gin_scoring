from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from gin_scoring.models import GameResult, Player, User

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


async def get_last_game_results(
    *, user_id: int, db_session: "AsyncSession"
) -> "Sequence[GameResult]":
    stmt = (
        select(GameResult)
        .join(Player, GameResult.player_north_id == Player.id)
        .join(User, Player.user_id == User.id)
        .filter(User.id == user_id)
        .order_by(GameResult.created_at.desc())
        .limit(10)
        .options(
            joinedload(GameResult.player_north),
            joinedload(GameResult.player_south),
            joinedload(GameResult.winner),
        )
    )
    return (await db_session.scalars(stmt)).all()
