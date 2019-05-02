import datetime
from typing import List, Optional

from isoweek import Week

from app import db
from app.models import DayOff, Team

from sqlalchemy import extract


def get_days_off(
    team_id: int, start_week: Optional[int] = None, end_week: Optional[int] = None
) -> List[DayOff]:
    """
    Returns all the hours taken off between two week ordinals, if they are
    provided.
    :param team_id: ID of the team for which to fetch days off.
    :param start_week: The lower bound for the days off taken, which is ignored
        if it is none.
    :param end_week: The lower bound for the days off taken, which is ignored if
        it is none.
    :return: Returns a list of days off in the date range. Any week not included
        is assumed to have no hours off.
    :
    """
    session = db.get_session()

    query = session.query(DayOff).filter(DayOff.team_id == team_id)
    if start_week:
        query = query.filter(DayOff.week >= start_week)
    if end_week:
        query = query.filter(DayOff.week <= end_week)

    return query.all()

def get_from_team_date(team: Team, date: datetime.date):
    session = db.get_session()
    return session.query(DayOff).filter(
        DayOff.team_id == team.id,
        DayOff.date == date
    ).one_or_none()

def get_days_off_by_year(team: Team, year: int):
    session = db.get_session()
    return session.query(DayOff).filter(
        DayOff.team_id == team.id,
        extract('year', DayOff.date) == year
    ).order_by(DayOff.date).all()

def delete_day_off(dayoff: DayOff):
    session = db.get_session()
    session.delete(dayoff)
    session.commit()

def set_day_off(team_id: int, date: datetime.date, hours_off: int) -> bool:
    """
    Set the number of hours off for a given day. If the number of hours off is
    set to 0, the entry is erased from the database, if already there.
    :param team_id: The ID of the team for which you're setting the day off
    :param date: Date to set
    :param hours_off: Number of hours off. Can be a number between 0 and 8
    :return: True if there were no issues. False if either the team does not
        exist, or an invalid number of hours were sent.
    """
    session = db.get_session()

    team = session.query(Team).filter(Team.id == team_id).one_or_none()
    if not team:
        return False
    if hours_off < 0 or hours_off > 8:
        return False

    week = Week.withdate(date).toordinal()
    day_off = (
        session.query(DayOff)
        .filter(DayOff.date == date)
        .filter(DayOff.team_id == team_id)
        .one_or_none()
    )
    if day_off:
        if hours_off == 0:
            session.delete(day_off)
        else:
            day_off.hours_off = hours_off
    elif hours_off != 0:
        session.add(DayOff(team=team, date=date, hours_off=hours_off, week=week))
    session.commit()

    return True
