from functools import cached_property

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.aliases import int_pk, str_50, small_int, created_at
from db.base import Base


class GameResult(Base):
    __tablename__ = "game_results"

    id: Mapped[int_pk]
    player_north_name: Mapped[str_50]
    player_south_name: Mapped[str_50]
    outcome: Mapped[str] = mapped_column(String(10))
    # These 2 ones can be `null` when the outcome is `draw`:
    winner_name: Mapped[Optional[str_50]]
    deadwood_value: Mapped[small_int]
    # Computed from the previous `end_type` and `deadwood_value` fields:
    winner_score: Mapped[Optional[small_int]]

    created_at: Mapped[created_at]

    @property
    def is_draw(self) -> bool:
        return self.outcome == "draw"

    @cached_property
    def loser_name(self) -> str:
        return [name for name in (self.player_north_name, self.player_south_name) if name != self.winner_name][0]

    def __str__(self) -> str:
        return f"{self.player_north_name.title()} vs {self.player_south_name.title()}, on {self.created_at.strftime('%a %d %b at %H:%M')}"
