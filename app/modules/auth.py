import requests
from flask import Blueprint, session, current_app, abort, jsonify, make_response, redirect, request, url_for, render_template, g

import urllib.parse as urlparse
from secrets import token_urlsafe

bp = Blueprint('auth', __name__)

from app.helpers import req_helper
from app.helpers import graph_api_helper
from app.helpers import session_helper

from app.models.util import token as token_util
from app.models.util import user  as user_util

url_auth_base = 'https://login.microsoftonline.com/common/oauth2/v2.0/'
url_authorize = 'authorize/'
url_token = 'token/'

@bp.route('/login-notice')
def login_notice():
    return render_template('card.html', title="Login Notice!", cards=[
            {
                'title': "You must be logged in to do this!",
                'text': [
                    'Please Log In and try again.',
                    'By logging in you agree to have cookies stored in your computer and for us to store basic personal information.'
                ],
                'icon': '<i class="fas fa-sign-in-alt"></i>',
                'link': {
                    'text': 'Click Here to Log In',
                    'href': url_for('auth.login')
                }
            },
        ])

@bp.route('/login')
# @session_helper.enforce_validate_token
@session_helper.load_user_if_logged_in
def login():
    if g.user:
        return redirect('/')
    else:
        return render_template('login.html')

@bp.route('/logout', methods=['GET', 'POST'])
@session_helper.enforce_validate_token
def logout():
    token = session_helper.retirieve_token()
    session_helper.destroy_session()
    token_util.destroy_token(token)
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        return jsonify(error=0, message="You logged out!")

@bp.route("/msft/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")
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
            token = token_urlsafe(128)
            session['schedulr_token'] = token

            user = user_util.get_or_create_user(name=user_data['name'], email=user_data['email'])
            token_util.save_token(user_id=user.id, token=token)

            user_data['token'] = token

            return redirect('/')

    