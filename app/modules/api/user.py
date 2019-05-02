from isoweek import Week
from flask import Blueprint, jsonify, g, request

from app.helpers import api_error_helpers, session_helper, req_helper

from app.models.util import (
    user as user_util,
    join_token as join_token_util,
    schedule as schedule_util,
    team as team_util
)

bp = Blueprint("api.user", __name__)


@bp.route("/<int:user_id>", methods=["GET"])
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


@bp.route("/setteam", methods=["POST"])
@req_helper.api_check_json("team_id")
@session_helper.enforce_validate_token_api
def set_team(json_content):
    join_token = join_token_util.by_team_id(json_content["team_id"])

    if not join_token:
        return api_error_helpers.item_not_found(
            "join_token", "team_id", json_content["team_id"]
        )

    if join_token.token_str != json_content["join_token"]:
        return api_error_helpers.invalid_join_token()

    user = user_util.set_team(g.user.id, json_content["team_id"])

    if user:
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "team_id": user.team.id,
            }
        )

    return api_error_helpers.could_not_update("user", "id", g.user.id)


@bp.route("/jointeam", methods=["POST"])
@req_helper.api_check_json("join_token")
@session_helper.enforce_validate_token_api
def join_team_token(json_content):
    team = join_token_util.team_by_join_token(json_content["join_token"])
    join_token = team.join_tokens[0] if team.join_tokens else None

    if not join_token:
        return api_error_helpers.item_not_found(
            "join token", "token", json_content["join_token"]
        )

    user_util.set_team(g.user.id, team.id)
    return jsonify(
        {
            "id": g.user.id,
            "name": g.user.name,
            "email": g.user.email,
            "team_id": g.user.team.id,
        }
    )


@bp.route("/register-many", methods=["POST"])
@req_helper.api_check_json("project_id", "iso_week", "hours")
@session_helper.enforce_validate_token_api
def loh_many_hours(json_content):
    if (
        isinstance(json_content["iso_week"], list)
        and isinstance(json_content["hours"], list)
        and isinstance(json_content["project_id"], list)
        and len(json_content["iso_week"]) == len(json_content["hours"])
        and len(json_content["iso_week"]) == len(json_content["project_id"])
    ):
        responses = []
        print(json_content["project_id"])
        print(json_content["iso_week"])
        print(json_content["hours"])
        for project_id, wk, hours in zip(
            json_content["project_id"], json_content["iso_week"], json_content["hours"]
        ):
            print(project_id, wk, hours)
            try:
                project_id = int(project_id)
                wk = Week.fromstring(wk)
                hours = int(hours)
                assert hours >= 0
            except:
                responses.append({"success": False})
                continue

            sched = schedule_util.set_schedule(
                g.user.id, project_id, wk.toordinal(), hours
            )

            if sched:
                responses.append(sched)
            else:
                responses.append({"success": False})

        return jsonify(responses)

    else:
        api_error_helpers.invalid_body_arg(["project_id", "iso_week", "hours"])


@bp.route("/register", methods=["POST"])
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
        assert hours >= 0
    except ValueError:
        return api_error_helpers.invalid_body_arg("hours")
    except AssertionError:
        return api_error_helpers.invalid_body_arg("hours")

    # Returns serialized result
    sched = schedule_util.set_schedule(g.user.id, project_id, wk.toordinal(), hours)

    if sched:
        return jsonify(sched)

    return api_error_helpers.could_not_create("schedule")


@bp.route("/<int:user_id>/sparse_schedule", methods=["GET"])
@session_helper.enforce_validate_token_api
def get_sparse_schedule(user_id: int):
    if not user_util.get_from_id(user_id):
        return api_error_helpers.item_not_found("user", "id", user_id)

    start_str = request.args.get("start_week", default=None, type=str)
    end_str = request.args.get("end_week", default=None, type=str)
    year = request.args.get("year", default=None, type=int)

    if (start_str or end_str) and year:
        return api_error_helpers.invalid_url_args_combination(
            ["start_str", "end_str", "year"]
        )
    if not ((start_str and end_str) or year):
        if not (start_str and end_str):
            return api_error_helpers.missing_url_arg("start_week and end_week")
        else:
            return api_error_helpers.missing_url_arg("year")

    start_week = Week.fromstring(start_str).toordinal() if start_str else None
    end_week = Week.fromstring(end_str).toordinal() if end_str else None

    if year:
        start_week = Week(year, 1)
        end_week = Week.last_week_of_year(year)

    schedule_map = schedule_util.get_user_schedules(user_id, start_week, end_week)

    return jsonify(list(sched.serialize() for sched in schedule_map.values()))


@bp.route("/<int:user_id>/schedule", methods=["GET"])
@session_helper.enforce_validate_token_api
def get_schedule(user_id: int):
    if not user_util.get_from_id(user_id):
        return api_error_helpers.item_not_found("user", "id", user_id)

    if g.user.id != user_id:
        return api_error_helpers.not_authorized()
    
    year = request.args.get("year", default=None, type=int)

    if not year:
        return api_error_helpers.missing_url_arg("year")

    start_week = Week(year, 1)
    end_week = Week.last_week_of_year(year)

    user_projects = user_util.get_projects_for_period(
        user_id=user_id, start_week=start_week, end_week=end_week
    )

    project_index = {proj.id: index for index, proj in enumerate(user_projects)}

    full_schedule = [
        [0 for project in user_projects] for week in Week.weeks_of_year(year)
    ]

    schedule_dict = schedule_util.get_user_schedules(
        user_id, start_week.toordinal(), end_week.toordinal()
    )

    for week_project, schedule in schedule_dict.items():
        week_index = Week.fromordinal(week_project.week).week - 1
        full_schedule[week_index][
            project_index[week_project.project_id]
        ] = schedule.hours

    work_hours = team_util.get_year_workhours(g.user.team.id, year)
    
    return jsonify(
        projects=list(map(lambda x: x.serialize(), user_projects)),
        schedule=full_schedule,
        work_hours=work_hours
    )
