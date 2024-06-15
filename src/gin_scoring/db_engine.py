import contextlib
import functools
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import get_settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine(str(get_settings().database_url))


@functools.cache
def get_session_maker() -> async_sessionmaker:
    return async_sessionmaker(engine)


async def get_db() -> "AsyncGenerator[AsyncSession, None, None]":
    async with get_session_maker() as session:
        yield session


get_db_context = contextlib.asynccontextmanager(get_db)
