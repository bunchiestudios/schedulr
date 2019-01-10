
from flask import g, current_app
import sqlalchemy

def get_db():
    if 'db' not in g:
        # TODO: do db stuff?
        pass
    return g.db