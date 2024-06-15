from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from .db_engine import get_db
from .settings import Settings, get_settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

# ruff: noqa: TCH003


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated["AsyncSession", Depends(get_db)]
