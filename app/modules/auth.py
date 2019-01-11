import requests
from flask import Blueprint, session, current_app, abort, jsonify, make_response, redirect, request, url_for

import urllib.parse as urlparse
from secrets import token_urlsafe

bp = Blueprint('auth', __name__)

from app.helpers import req_helper
from app.helpers import graph_api_helper

url_auth_base = 'https://login.microsoftonline.com/common/oauth2/v2.0/'
url_authorize = 'authorize/'
url_token = 'token/'

@bp.route('/login')
def login():
    # TODO: check token is valid, session_helper?
    if not session.get('schedulr_token'):
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
        # No code, therefore redirect to authorization url
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
            # Code failed to retrieve token
            # TODO: Render something here?
            abort(make_response(jsonify(message="Invalid code!"), 401))
        else:
            # Token is valid -> good login
            # Extract token
            data = r.json()
            access_token = data.get("access_token")

            # Retrieve user data from graph API
            user_data = graph_api_helper.get_user_data(access_token)
            # TODO: revoke token

            # Create a session
            session['schedulr_token'] = token_urlsafe(128)

            # TODO: check if user in database, if not create it, save token, save user id in cookie for quick lookup in BD?

            #TODO: redirect to main?
            return jsonify(message='Ok', data=user_data)

    