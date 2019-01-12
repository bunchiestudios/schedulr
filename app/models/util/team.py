from typing import Optional

from app import db
from app.models import Team

def get_from_id(team_id: int) -> Optional[Team]:
    session = db.get_session()
    return session.query(Team).filter(Team.id == team_id).one_or_none()

def create(name: str) -> Team:
    session = db.get_session()
    team = Team(name=name)
    session.add(team)
    session.commit()
    return team
