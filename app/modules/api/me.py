
from flask import Blueprint, jsonify, g, make_response
import secrets

from app.helpers import api_error_helpers, session_helper, req_helper

from app.models.util import (
    team as team_util,
    join_token as join_token_util,
)

from app.modules.api import (
    team as team_api,
    user as user_api,
)

bp = Blueprint('api.me', __name__)

# Returns user's team data
@bp.route('/team', methods=['POST'])
@session_helper.enforce_validate_token_api
def get_own_team():
    team = g.user.team
    if team is None:
        return api_error_helpers.item_not_found(item_name='Team-User', field_name='user-id', field_value='g.user.id')
    return jsonify(
        {
            "id": team.id,
            "name": team.name,
            "team_members": [user.id for user in team.users],
            "projects": [project.id for project in team.projects],
            "owner_id": team.owner.id,
            "user_is_owner": g.user.id == team.owner_id
        }
    )

@bp.route('/team/chart-data', methods=['GET'])
@session_helper.enforce_validate_token_api
def get_own_team_schedules():
    team = g.user.team
    if team is None:
        return api_error_helpers.item_not_found(item_name='Team-User', field_name='user-id', field_value='g.user.id')
    return team_api.team_get_chart_data(team.id)


@bp.route('/schedule', methods=['GET'])
@session_helper.enforce_validate_token_api
def get_own_schedule():
    return  user_api.get_schedule(user_id=g.user.id)
