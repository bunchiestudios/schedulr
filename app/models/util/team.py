from typing import Optional

from app import db
from app.models import Team, User
from app.models.util.user import set_team

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

    team = Team(name=name, owner=owner)
    session.add(team)
    session.commit()
    set_team(owner.id, team.id)
    return team
