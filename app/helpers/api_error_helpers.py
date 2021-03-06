from typing import List

from flask import Response, make_response, jsonify


def item_not_found(item_name: str, field_name: str, field_value: str) -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 1,
                    "msg": f"Could not find {item_name} with "
                    f'{field_name}="{field_value}"',
                }
            }
        ),
        404,
    )


def could_not_update(item_name: str, field_name: str, field_value: str) -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 2,
                    "msg": f"Could not update {item_name} for "
                    f'"{field_name}={field_value}"',
                }
            }
        ),
        404,
    )


def could_not_create(item_name: str) -> Response:
    return make_response(
        jsonify({"error": {"code": 3, "msg": f"Could not create {item_name}"}}), 400
    )


def not_authorized() -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 4,
                    "msg": "You are not authorized to perform this operation.",
                }
            }
        ),
        401,
    )


def invalid_join_token() -> Response:
    return make_response(
        jsonify({"error": {"code": 5, "msg": "The join token provided is invalid."}}),
        401,
    )


def is_not_json() -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 6,
                    "msg": "The request does not contain a valid JSON body.",
                }
            }
        ),
        400,
    )


def bad_body_arg() -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 7,
                    "msg": "Your request JSON body contains invalid data.",
                }
            }
        ),
        400,
    )


def missing_json_arg(arg_missing: str) -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 8,
                    "msg": f"Your JSON request is missing argument: {arg_missing}.",
                }
            }
        ),
        400,
    )


def invalid_body_arg(bad_arg: str) -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 9,
                    "msg": "Your JSON request passed an incorrect value for "
                    f"argument {bad_arg}",
                }
            }
        ),
        400,
    )


def invalid_url_arg(bad_arg: str) -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 10,
                    "msg": "Your GET request passed an incorrect value for "
                    f"argument {bad_arg}",
                }
            }
        ),
        400,
    )


def invalid_url_args_combination(bad_args: List[str]) -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 11,
                    "msg": "Your GET request passed an incorrect combination of "
                    f"values for the arguments {bad_args}",
                }
            }
        ),
        400,
    )


def missing_url_arg(missing_arg: str) -> Response:
    return make_response(
        jsonify(
            {
                "error": {
                    "code": 12,
                    "msg": "Your GET request is missing the URL argument "
                    f"{missing_arg}",
                }
            }
        ),
        400,
    )
