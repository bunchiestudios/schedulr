from flask import Blueprint, current_app
from sqlalchemy import create_engine

bp = Blueprint('setup', __name__)

@bp.route('/', methods=['POST'])
def setup():
    engine = create_engine(current_app.config['DB_STRING'], echo=False)
    tables.Base.metadata.create_all(engine)
    return "<h1> Created DB successfully! </h1>"