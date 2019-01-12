from flask import Blueprint, request, jsonify, Response
import json

from app import db
from app import models
from app.helpers import error_helpers, session_helper
from app.models.util import project as project_util, user as user_util


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


@bp.route('/user/<int:user_id>', methods=['GET'])
@session_helper.enforce_validate_token_api
def user_get(user_id):
    user = user_util.get_from_id(user_id)

    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email})

    return error_helpers.item_not_found("user", "id", str(user_id))
