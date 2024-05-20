import functools

from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict


@functools.cache
def get_settings() -> "Settings":
    return Settings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.local")

    database_url: Url
