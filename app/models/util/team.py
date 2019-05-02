from typing import Optional, List

from app import db
from app.models import Team, User, DayOff
from app.models.util.user import set_team

from isoweek import Week

from sqlalchemy import func, extract


def get_from_id(team_id: int) -> Optional[Team]:
    session = db.get_session()
    return session.query(Team).filter(Team.id == team_id).one_or_none()


def set_owner(team_id: int, owner_id: int) -> Optional[Team]:
    session = db.get_session()
    team = session.query(Team).filter(Team.id == team_id).one_or_none()
    owner = session.query(User).filter(User.id == owner_id).one_or_none()

    if not team or not owner:
        return None

    team.owner = owner
    session.commit()
    return team


def create(name: str, owner_id: int) -> Optional[Team]:
    session = db.get_session()
    owner = session.query(User).filter(User.id == owner_id).one_or_none()
    if not owner:
        return None

    team = Team(name=name, owner=owner, users=[owner])
    session.add(team)
    session.commit()
    set_team(owner.id, team.id)
    return team


def get_year_workhours(team_id: int, year: int) -> List[int]:
    session = db.get_session()

    weeks = (
        session.query(
            DayOff.week.label("ordinal_week"),
            func.sum(DayOff.hours_off).label("hours_off"),
        )
        .filter(DayOff.team_id == team_id, extract("year", DayOff.date) == year)
        .group_by(DayOff.week)
        .all()
    )

    work_hours = [40 for _ in Week.weeks_of_year(year)]

    for item in weeks:
        week_index = Week.fromordinal(item.ordinal_week).week - 1
        work_hours[week_index] -= int(item.hours_off)

    return work_hours
