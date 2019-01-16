from functools import wraps

from flask import request, abort, current_app, make_response, jsonify

from app.helpers import api_error_helpers

def api_check_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.json
        if data is None:
            abort(api_error_helpers.is_not_json())
        return func(json_content=data, *args, **kwargs)

    return wrapper