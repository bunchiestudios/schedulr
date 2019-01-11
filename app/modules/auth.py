import requests
from flask import Blueprint, session, current_app, abort, jsonify, make_response, redirect, request, url_for

import urllib.parse as urlparse

bp = Blueprint('auth', __name__)

from app.helpers import req_helper

url_auth_base = 'https://login.microsoftonline.com/common/oauth2/v2.0/'
url_authorize = 'authorize/'
url_token = 'token/'

@bp.route('/login')
def login():
    if not session.get("access_token"):
        return redirect(url_for('auth.callback'))
    else:
        redirect('/')

@bp.route("/msft/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")
    print('HELLO')
    if error:
        # TODO: render something here?
        return "Login Error"
    if not code:
        params = {
            'client_id': current_app.config['MSFT_APP_ID'],
            'redirect_uri': request.base_url,
            'response_type': 'code',
            'response_mode': 'query',
            'scope': 'openid User.Read'
        }
        return redirect(url_auth_base + url_authorize + '?' + urlparse.urlencode(params))
    else:
        r = requests.post(url_auth_base + url_token, data={
            'client_id': current_app.config['MSFT_APP_ID'],
            'client_secret': current_app.config['MSFT_APP_SECRET'],
            'grant_type':'authorization_code',
            'code': code,
            'redirect_uri': request.base_url
        })

        if r.status_code is not 200:
            # TODO: Render something here?
            abort(make_response(jsonify(message="Invalid code!"), 401))
        else:
            # Token is valid -> good login
            # TODO: check if user in database, if not create it, make a token and 
            data = r.json()
            session["access_token"] = data.get("access_token")
            return jsonify(message='Ok')

    