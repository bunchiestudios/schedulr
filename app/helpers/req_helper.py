from functools import wraps

from flask import request, abort, current_app, make_response, jsonify
from datetime import datetime
from functools import wraps, update_wrapper

def force_json_key_list(*args):
    data = request.json
    if data is None:
        abort(make_response(jsonify(message="No JSON provided!"), 400))
    for arg in args:
        if arg not in data:
            abort(make_response(jsonify(message="Missing data!", debug=f"Key not found: '{arg}'"), 400))
    return data


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)
from app.helpers import api_error_helpers


def api_check_json(*req_args):
    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.json
            if data is None:
                abort(api_error_helpers.is_not_json())
            for arg in set(req_args):
                if arg not in dict(data).keys():
                    abort(api_error_helpers.missing_json_arg(arg))
            return func(json_content=data, *args, **kwargs)
        return wrapper
    return wrap
