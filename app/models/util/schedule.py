from typing import Dict, List, NamedTuple, Optional, Tuple

from app import db
from app.models import Project, Schedule, User, Team
from sqlalchemy import func


class WeekProject(NamedTuple):
    week: int
    project_id: int


class WeekUser(NamedTuple):
    week: int
    user_id: int

def set_many(data: List[Tuple[int]]) -> List[Optional[Schedule]]:
    pass

def set_schedule(
    user_id: int, project_id: int, week: int, hours: int
) -> Optional[Schedule]:
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

    # Look for previous entry
    prev = session.query(Schedule).filter(Schedule.user_id == user_id, Schedule.project_id == project_id, Schedule.week == week).one_or_none()

    if prev is not None:
        if hours > 0:
            prev.hours = hours
            session.commit()
            return prev.serialize()
        else:
            session.delete(prev)
            session.commit()
            return {'success': True}
    else:
        if hours > 0:
            schedule = Schedule(user=user, project=project, week=week, hours=hours)
            session.add(schedule)
            session.commit()
            return schedule.serialize()
        else:
            return {'success': True}


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

    return (
        session.query(Schedule)
        .filter(
            Schedule.user_id == user_id,
            Schedule.project_id == project_id,
            Schedule.week == week,
        )
        .one_or_none()
    )


def get_user_schedules(
    user_id: int, start: int, end: int
) -> Dict[WeekProject, Schedule]:
    """
    Returns all the schedules for a given user by week, filtered by weeks.
    :param user_id: ID of the user for which to get schedules.
    :param start: The lower bound (inclusive) for the dates, or None if there is
        no lower bound.
    :param end: The upper bound (inclusive) for the dates, or None if there is
        no upper bound.
    :returns: A dictionary of schedules for the user in a, key-ed by
        week-project pairs, which are enforced to be unique in the API.
    """
    session = db.get_session()

    schedules = (
        session.query(Schedule)
        .filter(Schedule.user_id == user_id)
        .filter(Schedule.week >= start)
        .filter(Schedule.week <= end)
        .all()
    )

    return {WeekProject(sched.week, sched.project_id): sched for sched in schedules}


def get_project_schedules(project_id: int) -> Dict[WeekUser, Schedule]:
    """
    Returns all schedules for a given project.
    :param project_id: The ID of the project for which to get schedules.
    :returns: A dictionary of the schedules of a given project, key-ed by
        user-week pairs.
    """
    session = db.get_session()

    schedules = session.query(Schedule).filter(Schedule.project_id == project_id).all()

    return {WeekUser(sched.week, sched.user_id): sched for sched in schedules}


def get_project_week_schedule(project_id: int, week: int) -> Dict[int, Schedule]:
    """
    Gets all the schedules of a given project for a given week any user who
    logged hours on that project for the week.
    :param project_id: The ID of the project being searched.
    :param week: The week for which to search for the schedule.
    :returns: The schedule for a given week and project, if one exists. None
        otherwise
    """
    session = db.get_session()

    schedules = (
        session.query(Schedule)
        .filter(Schedule.project_id == project_id, Schedule.week == week)
        .all()
    )

    return {sched.user_id: sched for sched in schedules}


def get_team_schedules(team_id: int, start: int, end: int) -> List[Schedule]:
    """
    Gets all the schedules for all the projects owned by a given team, filtered
    to fall between two weeks.
    :param team_id: The ID of the team from which schedules are being fetched.
    :param start: Start week of the filter, inclusive, as an ordinal ISO week date
    :param end: End week of the filter, inclusive, as an ordinal ISO week date
    :returns: A list of all schedules for said team.
    """
    session = db.get_session()

    return (
        session.query(Schedule)
        .join(Project)
        .filter(Project.team_id == team_id)
        .filter(Schedule.week >= start)
        .filter(Schedule.week <= end)
        .all()
    )


def get_team_summary_schedule(
    team_id: int, start: int, end: int, period: float
) -> List[Tuple]:
    """
    Get statistics on the schedules for a given team, with limits on dates, and
    a period over which averages and other similar statistics are calculated.
    :param team_id: The ID for the team to search for
    :param start: Start week of the filter, inclusive, as an ordinal ISO week date
    :param end: End week of the filter, inclusive, as an ordinal ISO week date
    :returns: The summary of the schedule as a list of 3-tuples. Each tuple
        contains the average number of hours worked by a given user on a given
        project, the user ID, and the project ID.
    """
    session = db.get_session()
    results = (
        session.query(func.sum(Schedule.hours) / period, User.name, Project.name)
        .filter(Project.team_id == team_id)
        .filter(Schedule.week >= start)
        .filter(Schedule.week <= end)
        .group_by(Schedule.user_id, Schedule.project_id)
        .join(User)
        .join(Project)
        .all()
    )
    return results
