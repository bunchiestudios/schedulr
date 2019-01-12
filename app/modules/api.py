from flask import Blueprint, request, jsonify, Response, g
import json

import secrets

from app import db
from app import models
from app.helpers import error_helpers, session_helper
from app.models.util import (
    project as project_util,
    user as user_util,
    team as team_util,
    join_token as join_token_util
)


bp = Blueprint('api', __name__)


@bp.route('/project/<int:project_id>', methods=['GET'])
@session_helper.enforce_validate_token_api
def project_get(project_id):
    project = project_util.get_project_by_id(project_id)
    if project:
        return jsonify(
            {"id": project.id, "team_id": project.team_id, "name": project.name}
        )
    return error_helpers.item_not_found("project", "id", str(project_id))

@bp.route('/project', methods=['POST'])
@session_helper.enforce_validate_token_api
def project_post():
    name = request.args['name']
    team_id = request.args['team_id']

    project = project_util.add_project(name, team_id)
    if project:
        return jsonify(
            {"id": project.id, "team_id": project.team_id, "name": project.name}
        )
    return error_helpers.could_not_create("project")


@bp.route('/user/<int:user_id>', methods=['GET'])
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

    return error_helpers.item_not_found("user", "id", str(user_id))

@bp.route('/team/<int:team_id>', methods=['GET'])
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

    return error_helpers.item_not_found("team", "id", str(team_id))


@bp.route('/team/<int:team_id>/owner', methods=['POST'])
@session_helper.enforce_validate_token_api
def team_transfer_owner(team_id):
    team = team_util.get_from_id(team_id)
    owner_id = request.args['owner_id']

    if not team:
        return error_helpers.item_not_found("team", "id", str(team_id))

    if team.owner.id != g.user.id:
        return error_helpers.not_authorized()

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


@bp.route('/team', methods=['POST'])
@session_helper.enforce_validate_token_api
def team_create():
    team = team_util.create(request.args['name'], g.user.id)

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

    return error_helpers.item_not_found("user", "id", str(g.user.id))


# Ideally this would be a GET request, but browser will cache responses, and
# this _could_ have side-effects if no token exists already.
@bp.route('/team/<int:team_id>/join_token', methods=['POST'])
@session_helper.enforce_validate_token_api
def get_join_token(team_id):
    team = team_util.get_from_id(team_id)

    if not team:
        return error_helpers.item_not_found("team", "id", str(team_id))

    if g.user.id != team.owner_id:
        error_helpers.not_authorized()

    join_token = join_token_util.by_team_id(team_id)

    if not join_token:
        # Statistically unlikely that we'll ever get repeated tokens
        join_token = join_token_util.add_to_team(team_id, secrets.token_urlsafe(128))

        if not join_token:
            return error_helpers.item_not_found("team", "id", str(team_id))

    return jsonify(join_token.serialize())


@bp.route('/team/<int:team_id>/join_token/new', methods=['POST'])
@session_helper.enforce_validate_token_api
def get_new_join_token(team_id):
    team = team_util.get_from_id(team_id)

    if not team:
        return error_helpers.item_not_found("team", "id", str(team_id))

    join_token = join_token_util.add_to_team(team_id, secrets.token_urlsafe(128))

    if not join_token:
        return error_helpers.item_not_found("team", "id", str(team_id))

    return jsonify(join_token.serialize())


@bp.route('/user/team', methods=['POST'])
@session_helper.enforce_validate_token_api
def set_team():
    join_token = join_token_util.by_team_id(request.args['team_id'])
    
    if not join_token:
        return error_helpers.item_not_found('join_token', 'team_id', request.args['team_id'])

    if join_token.token_str != request.args['join_token']:
        return error_helpers.invalid_join_token()

    user = user_util.set_team(g.user.id, request.args['team_id'])

    if user:
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "team_id": user.team.id,
            }
        )

    return error_helpers.could_not_update('user', 'id', g.user.id)


@bp.route('/user/team/token', methods=['POST'])
@session_helper.enforce_validate_token_api
def join_team_token():
    team = join_token_util.team_by_join_token(request.args['join_token'])
    join_token = team.join_tokens[0] if team.join_tokens else None

    if not join_token:
        return error_helpers.item_not_found('join token', 'token', request.args['join_token'])

    user_util.set_team(g.user.id, team.id)
    return jsonify(
        {
            "id": g.user.id,
            "name": g.user.name,
            "email": g.user.email,
            "team_id": g.team.id,
        }
    )
