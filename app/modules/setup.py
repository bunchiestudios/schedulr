from app import db
from app import models
from flask import Blueprint

bp = Blueprint('setup', __name__)

@bp.route('/', methods=['POST'], strict_slashes=False)
def setup():
    models.Base.metadata.create_all(db.get_engine())
    return "<h1> Created DB successfully! </h1>"
