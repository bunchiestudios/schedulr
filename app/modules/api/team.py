from flask import Blueprint, jsonify, g, request, url_for

from dateutil.parser import parse as date_parse
from isoweek import Week
import secrets

from app.helpers import api_error_helpers, session_helper, req_helper
from app.models.util import (
    days_off as days_off_util,
    team as team_util,
    join_token as join_token_util,
    schedule as schedule_util,
)

from isoweek import Week

bp = Blueprint("api.team", __name__)


@bp.route("/<int:team_id>", methods=["GET"])
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


@bp.route("/<int:team_id>/owner", methods=["POST"])
@req_helper.api_check_json("owner_id")
@session_helper.enforce_validate_token_api
def team_transfer_owner(team_id, json_content):
    team = team_util.get_from_id(team_id)
    owner_id = json_content["owner_id"]

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


@bp.route("/", methods=["POST"], strict_slashes=False)
@req_helper.api_check_json("name")
@session_helper.enforce_validate_token_api
def team_create(json_content):
    team = team_util.create(json_content["name"], g.user.id)

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
@bp.route("/<int:team_id>/join_token", methods=["POST"])
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

    # return jsonify(join_token.serialize())
    return jsonify(
        link=url_for("team.join_link", code=join_token.token_str, _external=True)
    )


@bp.route("/<int:team_id>/join_token/new", methods=["POST"])
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
    return jsonify(
        link=url_for("team.join_link", code=join_token.token_str, _external=True)
    )


@bp.route("/<int:team_id>/projects", methods=["POST"])
@session_helper.enforce_validate_token_api
def team_get_projects(team_id):
    team = team_util.get_from_id(team_id)

    if team:
        return jsonify([project.serialize() for project in team.projects])

    return api_error_helpers.item_not_found("team", "id", str(team_id))


@bp.route("/<int:team_id>/days_off", methods=["GET"])
@session_helper.enforce_validate_token_api
def get_days_off(team_id: int):
    if not team_util.get_from_id(team_id):
        return api_error_helpers.item_not_found("team", "id", str(team_id))
    start_str = request.args.get("start_week", default=None, type=str)
    end_str = request.args.get("end_week", default=None, type=str)

    start_week = Week.fromstring(start_str).toordinal() if start_str else None
    end_week = Week.fromstring(end_str).toordinal() if end_str else None

    days_off = days_off_util.get_days_off(team_id, start_week, end_week)

    return jsonify([day_off.serialize() for day_off in days_off])


@bp.route("/<int:team_id>/day_off", methods=["POST"])
@req_helper.api_check_json("date", "hours_off")
@session_helper.enforce_validate_token_api
def set_days_off(team_id: int, json_content):
    team = team_util.get_from_id(team_id)

    if not team:
        return api_error_helpers.item_not_found("team", "id", str(team_id))

    try:
        date = date_parse(json_content["date"]).date()
        hours_off = int(json_content["hours_off"])
    except ValueError:
        return api_error_helpers.bad_body_arg()

    result = days_off_util.set_day_off(team_id, date, hours_off)
    if not result:
        return api_error_helpers.bad_body_arg()

    return jsonify({"result": "ok"})


@bp.route("/<int:team_id>/schedules", methods=["GET"])
@session_helper.enforce_validate_token_api
def team_get_schedules(team_id: int):
    if not team_util.get_from_id(team_id):
        return api_error_helpers.item_not_found("team", "id", str(team_id))

    start_ahead = request.args.get("start_ahead", default=None)
    look_ahead = request.args.get("look_ahead", default=0, type=int)
    try:
        start = Week.fromstring(start_ahead).toordinal()
    except ValueError:
        return api_error_helpers.invalid_url_arg("start_ahead")

    end = start + look_ahead
    if end < start:
        return api_error_helpers.invalid_url_arg('["start_ahead", "look_ahead"]')

    return jsonify(
        [
            schedule.serialize()
            for schedule in schedule_util.get_team_schedules(team_id, start, end)
        ]
    )


@bp.route("/<int:team_id>/chart-data", methods=["GET"])
@session_helper.enforce_validate_token_api
def team_get_chart_data(team_id):
    if not team_util.get_from_id(team_id):
        return api_error_helpers.item_not_found("team", "id", str(team_id))

    start_ahead = request.args.get("start_ahead", default=None)
    look_ahead = request.args.get("look_ahead", default=0, type=int)
    try:
        start = Week.fromstring(start_ahead).toordinal()
    except ValueError:
        return api_error_helpers.invalid_url_arg("start_ahead")
    end = start + look_ahead
    if end < start:
        return api_error_helpers.invalid_url_arg('["start_ahead","look_ahead"]')
    period = float(end - start + 1)
    results = schedule_util.get_team_summary_schedule(team_id, start, end, period)
    return jsonify(
        [
            {"user": item[1], "project": item[2], "hours": round(item[0], 2)}
            for item in results
        ]
    )
