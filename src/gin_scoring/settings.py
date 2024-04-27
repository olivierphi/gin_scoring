from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    database_url: str = "sqlite:///db.sqlite3"


settings = Settings()
