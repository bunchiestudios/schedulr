import requests
from flask import Blueprint, session, current_app, abort, jsonify, make_response, redirect, request, url_for, render_template, g

import urllib.parse as urlparse

bp = Blueprint('auth', __name__)

from app.helpers import req_helper
from app.helpers import graph_api_helper
from app.helpers import session_helper
from app.helpers import oauth_helper
from app.helpers import google_api_helper

from app.models.util import user  as user_util
from app.models.util import token as token_util


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
@session_helper.load_user_if_logged_in
def login():
    if g.user:
        return redirect('/')
    else:
        return render_template('login.html', title="Login", script="login.js")

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
def msft_callback():
    code = request.args.get("code")
    error = request.args.get("error")
    if error:
        # TODO: render something here?
        return "Login Error"
    oauth_client = oauth_helper.get_oauth_client_msft()
    if not code:
        # Make a Msft oauth client and redirect to auth url
        return redirect(oauth_client.get_authorization_url())
    else:
        try:
            access_token = oauth_client.request_token(code=code)
        except:
            abort(make_response(jsonify(message="Invalid code!"), 401))

        # Retrieve user data from graph API
        user_data = graph_api_helper.get_user_data(access_token)
        # TODO: revoke token

        # Makes or gets user with received data
        user = user_util.get_or_create_user(name=user_data['name'], email=user_data['email'])

        # Create session tied to this user
        session_helper.make_session(user=user)
        return redirect('/')

@bp.route("/google/callback")
def google_callback():
    code = request.args.get("code")
    error = request.args.get("error")
    if error:
        # TODO: render something here?
        return "Login Error"
    oauth_client = oauth_helper.get_oauth_client_google()
    if not code:
        # redirect to auth url
        return redirect(oauth_client.get_authorization_url())
    else:
        try:
            access_token = oauth_client.request_token(code=code)
            # Retrieve user data from graph API
        except:
            abort(make_response(jsonify(message="Invalid code!"), 401))
        
        user_data = google_api_helper.get_user_data(access_token)
        # TODO: revoke token

        # Makes or gets user with received data
        user = user_util.get_or_create_user(name=user_data['name'], email=user_data['email'])

        # Create session tied to this user
        session_helper.make_session(user=user)
        return redirect('/')
        

    