from flask import g, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def get_engine():
    return current_app.db_engine


def get_session() -> Session:
    if "db_session" not in g:
        g.db_session = current_app.db_Session()
    return g.db_session
