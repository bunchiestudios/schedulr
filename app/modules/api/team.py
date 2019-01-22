
from flask import Blueprint, jsonify, g, url_for
import secrets

from app.helpers import api_error_helpers, session_helper, req_helper

from app.models.util import (
    team as team_util,
    join_token as join_token_util
)

bp = Blueprint('api.team', __name__)

@bp.route('/<int:team_id>', methods=['GET'])
@session_helper.enforce_validate_token_api
def team_get(team_id):
    team = team_util.get_from_id(team_id)

    if team:
        return jsonify(
            {
                "id": team.id,
                "name": team.name,
                "team_members": [user.id for user in team.users],
                "projects": [project.id for project in team.projects],
                "owner_id": team.owner.id,
            }
        )

    return api_error_helpers.item_not_found("team", "id", str(team_id))


@bp.route('/<int:team_id>/owner', methods=['POST'])
@req_helper.api_check_json("owner_id")
@session_helper.enforce_validate_token_api
def team_transfer_owner(team_id, json_content):
    team = team_util.get_from_id(team_id)
    owner_id = json_content['owner_id']

    if not team:
        return api_error_helpers.item_not_found("team", "id", str(team_id))

    if team.owner_id != g.user.id:
        return api_error_helpers.not_authorized()

    team = team_util.set_owner(team.id, owner_id)

    if team:
        return jsonify(
            {
                "id": team.id,
                "name": team.name,
                "team_members": [user.id for user in team.users],
                "projects": [project.id for project in team.projects],
                "owner_id": team.owner.id,
            }
        )


@bp.route('/', methods=['POST'])
@req_helper.api_check_json("name")
@session_helper.enforce_validate_token_api
def team_create(json_content):
    team = team_util.create(json_content['name'], g.user.id)

    if team:
        return jsonify(
            {
                "id": team.id,
                "name": team.name,
                "team_members": [user.id for user in team.users],
                "projects": [project.id for project in team.projects],
                "owner_id": team.owner.id,
            }
        )

    return api_error_helpers.item_not_found("user", "id", str(g.user.id))


# Ideally this would be a GET request, but browser will cache responses, and
# this _could_ have side-effects if no token exists already.
@bp.route('/<int:team_id>/join_token', methods=['POST'])
@session_helper.enforce_validate_token_api
def get_join_token(team_id):
    team = team_util.get_from_id(team_id)

    if not team:
        return api_error_helpers.item_not_found("team", "id", str(team_id))

    if g.user.id != team.owner_id:
        return api_error_helpers.not_authorized()

    join_token = join_token_util.by_team_id(team_id)

    if not join_token:
        # Statistically unlikely that we'll ever get repeated tokens
        join_token = join_token_util.add_to_team(team_id, secrets.token_urlsafe(16))

        if not join_token:
            return api_error_helpers.item_not_found("team", "id", str(team_id))

    #return jsonify(join_token.serialize())
    return jsonify(link=url_for('team.join_link', code=join_token.token_str, _external=True))


@bp.route('/<int:team_id>/join_token/new', methods=['POST'])
@session_helper.enforce_validate_token_api
def get_new_join_token(team_id):
    team = team_util.get_from_id(team_id)

    if not team:
        return api_error_helpers.item_not_found("team", "id", str(team_id))

    if team.owner_id != g.user.id:
        return api_error_helpers.not_authorized()

    join_token = join_token_util.add_to_team(team_id, secrets.token_urlsafe(16))

    if not join_token:
        return api_error_helpers.item_not_found("team", "id", str(team_id))

    # return jsonify(join_token.serialize())
    return jsonify(link=url_for('team.join_link', code=join_token.token_str, _external=True))