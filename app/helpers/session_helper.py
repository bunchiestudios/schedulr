
from flask import session, url_for, redirect, abort, make_response, jsonify, current_app

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
            #TODO: check token against database
            return method(*args, **kwargs)
        else:
            return on_failure(400, "No token provided!")
    return wrapper

def enforce_validate_token(method):
    return __make_wrapper(method, 'redirect')

def enforce_validate_token_api(method):
    return __make_wrapper(method, 'error')
