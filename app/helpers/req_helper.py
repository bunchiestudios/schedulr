from functools import wraps

from flask import request, abort, current_app, make_response, jsonify
from app.helpers import api_error_helpers

def api_check_json(*req_args):
    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                abort(api_error_helpers.is_not_json())
            for arg in set(req_args):
                if arg not in dict(data).keys():
                    abort(api_error_helpers.missing_json_arg(arg))
            return func(json_content=data, *args, **kwargs)
        return wrapper
    return wrap
