from isoweek import Week
from flask import Blueprint, jsonify, g, request

from secrets import token_urlsafe

from app.helpers import api_error_helpers, session_helper, req_helper

from app.models.util import (
    user as user_util,
    join_token as join_token_util,
    schedule as schedule_util,
    token as token_util,
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


@bp.route('/register_hours', methods=['POST'])
@req_helper.api_check_json("project_id", "iso_week", "hours")
@session_helper.enforce_validate_token_api
def log_hours(json_content):
    try:
        project_id = int(json_content["project_id"])
    except ValueError:
        return api_error_helpers.invalid_body_arg("project_id")

    try:
        wk = Week.fromstring(json_content["iso_week"])
    except ValueError:
        return api_error_helpers.invalid_body_arg("iso_week")

    try:
        hours = int(json_content["hours"])
    except ValueError:
        return api_error_helpers.invalid_body_arg("hours")

    sched = schedule_util.set_schedule(g.user.id, project_id, wk.toordinal(), hours)
    
    if sched:
        return jsonify(sched.serialize())

    return api_error_helpers.could_not_create("schedule")


@bp.route('/<int:user_id>/schedule', methods=['GET'])
@session_helper.enforce_validate_token_api
def get_schedule(user_id: int):
    if not user_util.get_from_id(user_id):
        return api_error_helpers.item_not_found("user", "id", user_id)

    start_str = request.args.get('start_week', default=None)
    end_str = request.args.get('end_week', default=None)

    start_week = Week.fromstring(start_str).toordinal() if start_str else None
    end_week = Week.fromstring(end_str).toordinal() if end_str else None

    schedule_util.get_user_schedules(user_id, start_week, end_week)


@bp.route('/test_user', methods=['POST'])
@req_helper.api_check_json("name", "email")
@session_helper.test_api
def create_test_user(json_content):
    token = token_urlsafe(128)
    user = user_util.get_or_create_user(
        name=json_content["name"], email=json_content["email"]
    )
    if not token_util.save_token(user_id=user.id, token=token):
        return api_error_helpers.item_not_found("user", "id", str(user.id))

    return jsonify(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "team_id": user.team.id if user.team else None,
            "token": token,
        }
    )
