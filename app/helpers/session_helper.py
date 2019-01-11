
from flask import session, url_for, redirect, abort, make_response, jsonify, current_app

from app.models.util import token as token_utils
from app.models.util import user as user_utils

from app.models import User

session_key = 'schedulr_token'

def get_session_token_key():
    return session_key


def __make_on_failure(action):
    if action == 'error':
        def error_result(code, message):
            return abort(make_response(jsonify(message=message), code))
        return error_result
    elif action == 'redirect':
        def redirect_result(code, message):
            return redirect(url_for('auth.callback'))
        return redirect_result

def __make_wrapper(method, action):
    on_failure = __make_on_failure(action)
    def wrapper(*args, **kwargs):
        if session_key in session:
            token_str = session[session_key]
            token = token_utils.verify_token(token_str)
            if token is None:
                return on_failure(401, "Token is invalid!")
            if token_utils.older_than(token=token, hours=48):
                token_utils.destroy_token(token)
                return on_failure(401, "Token is too old!")
            user = user_utils.get_from_token(token)
            if user is None:
                token_utils.destroy_token(token)
                return on_failure(401, "Token is not associated with any user!")
            from flask import g
            g.user = user
            return method(*args, **kwargs)
        else:
            return on_failure(401, "No token provided!")
    return wrapper

def enforce_validate_token(method):
    return __make_wrapper(method, 'redirect')

def enforce_validate_token_api(method):
    return __make_wrapper(method, 'error')


def get_logged_in_user() -> User:
    if session_key in session:
        token_str = session[session_key]
        token = token_utils.verify_token(token_str)
        if token is None:
            return None
        if token_utils.older_than(token=token, hours=48):
            token_utils.destroy_token(token)
            return None
        user = user_utils.get_from_token(token)
        if user is None:
            token_utils.destroy_token(token)
            return None
        from flask import g
        g.user = user
        return user
    else:
        return None
