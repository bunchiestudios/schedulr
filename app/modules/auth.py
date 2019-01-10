
from flask import Blueprint
bp = Blueprint('test', __name__)

from app.helpers import req_helper

@bp.route("/login")
def login():
    data = req_helper.force_json_key_list('username', 'password')
    