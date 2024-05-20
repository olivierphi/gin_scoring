from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .db_engine import engine
from .settings import Settings, get_settings

if TYPE_CHECKING:
    from collections.abc import Generator

# ruff: noqa: TCH003


async def get_db() -> "Generator[AsyncSession, None, None]":
    async_session = async_sessionmaker(engine)
    async with async_session() as session:
        yield session


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_db)]
