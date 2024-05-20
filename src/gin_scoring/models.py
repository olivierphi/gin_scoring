import datetime as dt

from sqlalchemy import SmallInteger, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class GameResult(Base):
    __tablename__ = "game_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_north_name: Mapped[str] = mapped_column(String(50))
    player_south_name: Mapped[str] = mapped_column(String(50))
    outcome: Mapped[str]
    winner_name: Mapped[str | None] = mapped_column(String(50))
    deadwood_value: Mapped[int] = mapped_column(SmallInteger)
    winner_score: Mapped[int | None]
    created_at: Mapped[dt.datetime] = mapped_column(insert_default=func.now())
