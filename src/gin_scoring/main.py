import logging

from fastapi import FastAPI
from sqlalchemy import select

from .deps import SessionDep, SettingsDep
from .models import GameResult

# ruff: noqa: TCH001

app = FastAPI()


def configure_logging() -> None:
    # TODO: move this elsewhere ^^
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(logging.DEBUG)
    sqlalchemy_logger.addHandler(logging.getLogger("fastapi_cli").handlers[0])


configure_logging()


@app.get("/")
async def read_root(async_session: SessionDep, settings: SettingsDep):
    async with async_session as session:
        last_game = (await session.scalars(select(GameResult).limit(1))).first()
    return {
        "Hello": "World",
        "database_url": settings.database_url,
        "now_from_db": last_game.player_north_name if last_game else None,
    }
