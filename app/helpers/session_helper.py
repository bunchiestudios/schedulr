from functools import wraps
from secrets import token_urlsafe
from flask import (
    request,
    session,
    url_for,
    redirect,
    abort,
    make_response,
    jsonify,
    current_app,
)

from app.helpers import api_error_helpers
from app.models import User, Token
from app.models.util import token as token_utils
from app.models.util import user as user_utils

from app.models import User, Token


def get_session_token_key():
    return "schedulr_token"


def session_token_exists():
    return get_session_token_key() in session or 'X-Authorization' in request.headers


def get_session_token():
    if 'X-Authorization' in request.headers:
        return request.headers['X-Authorization']
    else:
        return session[get_session_token_key()]


def make_session(*, user: User):
    token = token_urlsafe(128)
    session[get_session_token_key()] = token
    token_utils.save_token(user_id=user.id, token=token)


def get_logged_in_user() -> User:
    from flask import g

    g.setdefault("user", None)
    if session_token_exists():
        token_str = get_session_token()
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
        g.user = user
        return user
    else:
        return None


def __make_on_failure(action):
    if action == "error":

        def error_result(code, message):
            return abort(make_response(jsonify(message=message), code))

        return error_result
    elif action == "redirect":

        def redirect_result(code, message):
            return redirect(url_for("auth.login"))

        return redirect_result


def __make_wrapper(method, action):
    on_failure = __make_on_failure(action)

    @wraps(method)
    def wrapper(*args, **kwargs):
        if session_token_exists():
            token_str = get_session_token()
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
    return __make_wrapper(method, "redirect")


def enforce_validate_token_api(method):
    return __make_wrapper(method, "error")


def load_user_if_logged_in(method):
    """Decorator: stores the user, if any, un g.user
    
    Arguments:
        method {func} -- Function to decorate
    
    Returns:
        func -- Decorated function.
    """

    @wraps(method)
    def wrapper(*args, **kwargs):
        get_logged_in_user()
        return method(*args, **kwargs)

    return wrapper


def test_api(func):
    """
    Decorator: Will search for the TEST_MODE config. If it is set to a truthy value,
    it will allow users through. Otherwise, it will throw an HTTP 401 error.
    :param func: Function to decorate
    :returns: New decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_app.config.get('TEST_MODE', None):
            return func(*args, **kwargs)
        return api_error_helpers.not_authorized()
    return wrapper

def retirieve_token() -> Token:
    return token_utils.verify_token(get_session_token())


def destroy_session():
    session.clear()
