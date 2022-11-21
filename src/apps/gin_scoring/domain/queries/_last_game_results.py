from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from sqlalchemy import select, desc

from db.session import db_session
from ...models import GameResult


def last_game_results() -> Sequence[GameResult]:
    stmt = select(GameResult).order_by(desc(GameResult.created_at)).limit(10)
    return db_session.execute(stmt).all()
