
from flask import Flask, g
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def create_app():
    # Setup flask app
    flapp = Flask(__name__)
    flapp.config.from_envvar('SCHEDULR_SETTINGS')

    # Setup SQLAlchemy engine & Session class
    flapp.db_engine = create_engine(flapp.config['DB_STRING'])
    flapp.db_Session = sessionmaker(bind=flapp.db_engine)

    # Setup blueprints
    from app.modules import test_module, auth, setup, home, team
    flapp.register_blueprint(test_module.bp, url_prefix='/test')
    flapp.register_blueprint(setup.bp, url_prefix='/setup')
    flapp.register_blueprint(auth.bp, url_prefix='/auth')
    flapp.register_blueprint(team.bp, url_prefix='/team')
    flapp.register_blueprint(home.bp, url_prefix='/')

    return flapp
