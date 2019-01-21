from typing import Dict, Optional, Tuple

from app import db
from app.models import Project, Schedule, User

def set_schedule(user_id: int, project_id: int, week: int, hours: int) -> Optional[Schedule]:
    """
    Logs the number of hours a given user plans to work on a given project for
    a given week. This will override existing values if present.
    :param user_id: The ID of the user that will be logged for these hours.
    :param project_id: The ID of the project on which the suer will work.
    :param week: The week number, where week 0 is the week staring on the 1st
        of January 1AD.
    :param hours: The number of hours to be logged for that week.
    :returns: The schedule created if none existed for that week/project
        combination, the exsting schedule if it was already present, or none if
        either the user_id or project_id did not correspond to this user, or if
        the user is not part of the project.
    """
    session = db.get_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()
    project = session.query(Project).filter(Project.id == project_id).one_or_none()

    if not user or not project:
        return None

    if project not in user.team.projects:
        return None

    schedule = session.query(Schedule).\
        filter(
            Schedule.project_id == project_id,
            Schedule.week == week,
        ).one_or_none()

    if schedule:
        return schedule

    schedule = Schedule(user=user, project=project, week=week, hours=hours)


def get_schedule(user_id: int, project_id: int, week: int) -> Optional[Schedule]:
    """
    Returns the schedule for a given user and project in a given week, if such
    a schedule exists.
    :param user_id: ID of the user for which to fetch the schedule.
    :param project_id: ID of the project for which to fetch the schedule.
    :param week: The week for which to fetch the schedule.
    :returns: The schedule if it exists, or None if it does not exist.
    """
    session = db.get_session()

    return session.query(Schedule).filter(
        Schedule.user_id == user_id,
        Schedule.project_id == project_id,
        Schedule.week == week,
    ).one_or_none()


def get_user_schedules(user_id: int) -> Dict[Tuple[int, int], Schedule]:
    """
    Returns all the schedules for a given user by week.
    :param user_id: ID of the user for which to get schedules.
    :returns: A dictionary of schedules for the user in a, key-ed by
        week-project pairs, which are enforced to be unique in the API.
    """
    session = db.get_session()

    schedules = session.query(Schedule).\
        filter(Schedule.user_id == user_id).all()

    return {(sched.project_id, sched.week): sched for sched in schedules}


def get_project_schedules(project_id: int) -> Dict[int, Schedule]:
    """
    Returns all schedules for a given project.
    :param project_id: The ID of the project for which to get schedules.
    :returns: A dictionary of the schedules of a given project, key-ed by week
        number.
    """
    session = db.get_session()

    schedules = session.query(Schedule).\
        filter(Schedule.project_id == project_id).all()

    return {sched.week: sched for sched in schedules}


def get_project_week_schedule(project_id: int, week: int) -> Optional[Schedule]:
    """
    Gets the schedule of a given project for a given week.
    :param project_id: The ID of the project being searched.
    :param week: The week for which to search for the schedule.
    :returns: The schedule for a given week and project, if one exists. None
        otherwise
    """
    session = db.get_session()

    return session.query(Schedule).\
        filter(Schedule.project_id == project_id, Schedule.week == week).\
        one_or_none()
