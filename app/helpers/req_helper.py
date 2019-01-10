from flask import request, abort, current_app, make_response, jsonify

def force_json_key_list(*args):
    data = request.json
    if data is None:
        abort(make_response(jsonify(message="No JSON provided!"), 400))
    for arg in args:
        if arg not in data:
            abort(make_response(jsonify(message="Missing data!", debug=f"Key not found: '{arg}'"), 400))
    return data