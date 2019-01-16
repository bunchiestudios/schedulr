from flask import jsonify, Response

def item_not_found(
    item_name: str, field_name: str, field_value: str
) -> Response:
    return Response(
        jsonify(
            {
                "error": {
                    "code": 1,
                    "msg": f'Could not find {item_name} with '
                    f'{field_name}="{field_value}"',
                }
            }
        ),
        status=404,
        mimetype="application/json",
    )

def could_not_update(
    item_name: str, field_name: str, field_value: str
) -> Response:
    return Response(
        jsonify(
            {
                "error": {
                    "code": 2,
                    "msg": f'Could not update {item_name} for '
                    f'"{field_name}={field_value}"',
                }
            }
        ),
        status=404,
        mimetype="application/json",
    )

def could_not_create(item_name: str) -> Response:
    return Response(
        jsonify(
            {
                "error": {
                    "code": 3,
                    "msg": f'Could not create {item_name}'
                }
            }
        ),
        status=400,
        mimetype="application/json",
    )

def not_authorized() -> Response:
    return Response(
        jsonify(
            {
                "error": {
                    "code": 4,
                    "msg": "You are not authorized to perform this operation."
                }
            }
        ),
        status=403,
        mimetype="application/json",
    )


def invalid_join_token() -> Response:
    return Response(
        jsonify(
            {
                "error": {
                    "code": 5,
                    "msg": "The join token provided is invalid."
                }
            }
        ),
        status=403,
        mimetype="application/json",
    )

def is_not_json() -> Response:
    return Response(
        jsonify(
            {
                "error": {
                    "code": 6,
                    "msg": "The request does not contain a JSON body."
                }
            }
        ),
        status=400,
        mimetype="application/json"
    )