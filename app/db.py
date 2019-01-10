
from flask import g, current_app
import sqlalchemy
from sqlalchemy.orm import sessionmaker

def get_engine():
    if 'db_engine' not in g:
        g.db_engine = sqlalchemy.create_engine(current_app.config['DB_STRING'])
    return g.db_engine

def get_session():
    if 'db_session' not in g:
        Session = sessionmaker(bind=get_engine())
        g.db_session = Session()
    return g.db_session
    
