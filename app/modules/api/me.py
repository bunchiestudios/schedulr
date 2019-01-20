
from flask import Blueprint, jsonify, g 
import secrets

from app.helpers import api_error_helpers, session_helper, req_helper

from app.models.util import (
    team as team_util,
    join_token as join_token_util
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
        id=team.id,
        name=team.name,
        owner_id=team.owner_id
    )