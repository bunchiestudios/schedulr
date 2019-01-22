
from flask import g, current_app, Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

def get_engine():
    return current_app.db_engine

def get_session() -> Session:
    if 'db_session' not in g:
        g.db_session = current_app.db_Session()
    return g.db_session


def init_app(app:Flask):
    @app.teardown_request
    def delete_session(exception):
        if 'db_session' in g:
            g.db_session.close()
