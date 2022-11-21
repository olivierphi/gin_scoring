import os

from sqlalchemy import create_engine

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_ECHO = bool(os.environ.get("DATABASE_ECHO", ""))
engine = create_engine(DATABASE_URL, echo=DATABASE_ECHO)
