from flask import Blueprint, jsonify

from app import db
from app import models
from app.helpers import session_helper
from app.models import Base

bp = Blueprint("setup", __name__)


@bp.route("/", methods=["POST"], strict_slashes=False)
@session_helper.test_api
def setup():
    models.Base.metadata.create_all(db.get_engine())
    return jsonify({"result": "ok"})


@bp.route("/clear_db", methods=["POST"])
@session_helper.test_api
def clear_db():
    Base.metadata.drop_all(bind=db.get_engine())
    return jsonify({"result": "ok"})
