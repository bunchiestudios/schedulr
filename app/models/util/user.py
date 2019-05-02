from typing import List, Optional

from app import db
from app.models import User, Team, Token, Project, Schedule

from isoweek import Week


def get_or_create_user(*, name: str, email: str) -> User:
    session = db.get_session()
    user = session.query(User).filter(User.email == email).one_or_none()
    if user:
        return user
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    return user


def get_from_token(token: Token) -> User:
    session = db.get_session()
    return session.query(User).filter_by(id=token.user_id).one_or_none()


def get_from_id(user_id: int) -> Optional[User]:
    session = db.get_session()
    return session.query(User).filter(User.id == user_id).one_or_none()


def remove_team(user_id: int) -> None:
    session = db.get_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()

    if not user:
        return None
    
    user._teams = []
    session.commit()
    

def set_team(user_id: int, team_id: int) -> Optional[User]:
    session = db.get_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()
    team = session.query(Team).filter(Team.id == team_id).one_or_none()

    if not user or not team:
        return None

    user._teams = [team]
    session.commit()

    return user


def get_projects(user_id: int) -> List[Project]:
    session = db.get_session()

    return session.query(Project).join(Team).join(User).filter(User.id == 1).all()


def get_projects_for_period(
    *, user_id: int, start_week: Week, end_week: Week
) -> List[Project]:
    session = db.get_session()

    return (
        session.query(Project)
        .filter(Schedule.user_id == user_id)
        .join(Schedule)
        .filter(Schedule.week >= start_week.toordinal())
        .filter(Schedule.week <= end_week.toordinal())
        .group_by(Schedule.project_id)
        .all()
    )
