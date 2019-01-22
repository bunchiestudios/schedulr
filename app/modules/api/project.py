from collections import defaultdict

from flask import Blueprint, jsonify, g 
from isoweek import Week

from app.helpers import api_error_helpers, session_helper, req_helper
from app.models import Schedule
from app.models.util import project as project_util, schedule as schedule_util

bp = Blueprint('api.project', __name__)

@bp.route('/<int:project_id>', methods=['GET', 'POST'])
@session_helper.enforce_validate_token_api
def project_get(project_id):
    project = project_util.get_project_by_id(project_id)
    if project:
        return jsonify(
            {"id": project.id, "team_id": project.team_id, "name": project.name}
        )
    return api_error_helpers.item_not_found("project", "id", str(project_id))

@bp.route('/', methods=['POST'], strict_slashes=False)
@req_helper.api_check_json("name", "team_id")
@session_helper.enforce_validate_token_api
def project_post(json_content):
    name = json_content['name']
    team_id = json_content['team_id']

    project = project_util.add_project(name, team_id)
    if project:
        return jsonify(
            {"id": project.id, "team_id": project.team_id, "name": project.name}
        )
    return api_error_helpers.could_not_create("project")


@bp.route('/<int:project_id>/schedules', methods=['GET'])
@session_helper.enforce_validate_token_api
def project_schedules(project_id: int):
    if not project_util.get_project_by_id(project_id):
        return api_error_helpers.item_not_found("project", "id", str(project_id))

    schedule_dict = schedule_util.get_project_schedules(project_id)

    return jsonify(
        [sched.serialize() for sched in schedule_dict.values()]
    )