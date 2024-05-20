from sqlalchemy.ext.asyncio import create_async_engine

from .settings import get_settings

engine = create_async_engine(str(get_settings().database_url))
