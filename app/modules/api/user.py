from flask import Blueprint, jsonify, g 

from app.helpers import api_error_helpers, session_helper, req_helper

from app.models.util import (
    user as user_util,
    join_token as join_token_util
)

bp = Blueprint('api.user', __name__)

@bp.route('/<int:user_id>', methods=['GET'])
@session_helper.enforce_validate_token_api
def user_get(user_id):
    user = user_util.get_from_id(user_id)

    if user:
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "team_id": user.team.id if user.team else None,
            }
        )

    return api_error_helpers.item_not_found("user", "id", str(user_id))

@bp.route('/setteam', methods=['POST'])
@req_helper.api_check_json("team_id")
@session_helper.enforce_validate_token_api
def set_team(json_content):
    join_token = join_token_util.by_team_id(json_content['team_id'])
    
    if not join_token:
        return api_error_helpers.item_not_found('join_token', 'team_id', json_content['team_id'])

    if join_token.token_str != json_content['join_token']:
        return api_error_helpers.invalid_join_token()

    user = user_util.set_team(g.user.id, json_content['team_id'])

    if user:
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "team_id": user.team.id,
            }
        )

    return api_error_helpers.could_not_update('user', 'id', g.user.id)


@bp.route('/jointeam', methods=['POST'])
@req_helper.api_check_json("join_token")
@session_helper.enforce_validate_token_api
def join_team_token(json_content):
    team = join_token_util.team_by_join_token(json_content['join_token'])
    join_token = team.join_tokens[0] if team.join_tokens else None

    if not join_token:
        return api_error_helpers.item_not_found('join token', 'token', json_content['join_token'])

    user_util.set_team(g.user.id, team.id)
    return jsonify(
        {
            "id": g.user.id,
            "name": g.user.name,
            "email": g.user.email,
            "team_id": g.user.team.id,
        }
    )