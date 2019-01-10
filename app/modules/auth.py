import requests
from flask import Blueprint, session, current_app
bp = Blueprint('auth', __name__)

from app.helpers import req_helper

@bp.route("/login")
def login():
    data = req_helper.force_json_key_list('code')
    requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data={
        'client_id': '6e1d68a4-6825-456e-bb73-df22d8d0d7ba',
    })

    