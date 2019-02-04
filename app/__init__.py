from flask import Flask, g
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from app.db import init_app


def create_app():
    # Setup flask app
    flapp = Flask(__name__)
    flapp.config.from_envvar("SCHEDULR_SETTINGS")

    # Setup SQLAlchemy engine & Session class
    flapp.db_engine = create_engine(flapp.config["DB_STRING"])
    flapp.db_Session = scoped_session(sessionmaker(bind=flapp.db_engine))

    init_app(flapp)

    # Setup blueprints
    from app.modules import test_module, auth, setup, home, team

    flapp.register_blueprint(test_module.bp, url_prefix="/test")
    flapp.register_blueprint(setup.bp, url_prefix="/setup")
    flapp.register_blueprint(auth.bp, url_prefix="/auth")
    flapp.register_blueprint(team.bp, url_prefix="/team")
    flapp.register_blueprint(home.bp, url_prefix="/")

    # Setup api
    from app.modules.api import (
        me as api_me,
        team as api_team,
        user as api_user,
        project as api_project,
    )

    flapp.register_blueprint(api_me.bp, url_prefix="/api/me")
    flapp.register_blueprint(api_team.bp, url_prefix="/api/team")
    flapp.register_blueprint(api_user.bp, url_prefix="/api/user")
    flapp.register_blueprint(api_project.bp, url_prefix="/api/project")

    return flapp
