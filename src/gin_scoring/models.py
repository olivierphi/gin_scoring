import datetime as dt

from sqlalchemy import ForeignKey, SmallInteger, String, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)

from .gin_rummy import GinRummyOutcome


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    players: Mapped[list["Player"]] = relationship(init=False, back_populates="user")
    is_active: Mapped[bool] = mapped_column(default=True)


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), init=False)
    user: Mapped[User] = relationship(back_populates="players")


class GameResult(Base):
    __tablename__ = "game_results"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    player_north_id: Mapped[int] = mapped_column(ForeignKey(Player.id), init=False)
    player_north: Mapped[Player] = relationship(foreign_keys=[player_north_id])
    player_south_id: Mapped[int] = mapped_column(ForeignKey(Player.id), init=False)
    player_south: Mapped[Player] = relationship(foreign_keys=[player_south_id])
    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey(Player.id), nullable=True, init=False
    )
    winner: Mapped[Player | None] = relationship(foreign_keys=[winner_id])
    outcome: Mapped[GinRummyOutcome] = mapped_column(SmallInteger)
    deadwood_value: Mapped[int] = mapped_column(SmallInteger)
    winner_score: Mapped[int | None]
    created_at: Mapped[dt.datetime] = mapped_column(insert_default=func.now())
