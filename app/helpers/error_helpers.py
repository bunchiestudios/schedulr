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
                    f'{field_name}="{field_value}"'
                }
            }
        ),
        status=404,
        mimetype="application/json",
    )
