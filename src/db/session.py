from sqlalchemy.orm import sessionmaker, scoped_session
from .engine import engine

# Managing SQLAlchemy (without the added magic of the Flask-SQLAlchemy extension)
# @link https://flask.palletsprojects.com/en/2.2.x/patterns/sqlalchemy/
orm_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(orm_session_maker)
