from typing import Optional

from app import db
from app.models import JoinToken, Team

def by_team_id(team_id: int) -> Optional[JoinToken]:
    """
    Returns existing join token for a given team.
    :param team_id: ID of the team to look for a join token of.
    :return: Returns a JoinToken object if the team exists and has one, or
             None otherwise.
    """
    session = db.get_session()
    team: Team = session.query(Team).filter(Team.id == team_id).one_or_none()
    if not team:
        return None

    return team.join_tokens[0] if team.join_tokens else None


def add_to_team(team_id: int, join_token_str: str) -> Optional[JoinToken]:
    """
    Adds a given join token to the team, replacing any existing join token.
    :param team_id: Team to which to add the join_token
    :param join_token_str: Join token string to add to the team.
    :return: Returns a JoinToken object if the team exists, or None otherwise.
    """

    session = db.get_session()
    team: Team = session.query(Team).filter(Team.id == team_id).one_or_none()

    if not team:
        return None

    # This gets rid of the tokens and deletes the relationship as well
    if team.join_tokens:
        for join_token in team.join_tokens:
            session.delete(join_token)
    
    join_token = JoinToken(token_str=join_token_str)
    team.join_tokens = [join_token]
    session.add(join_token)
    session.commit()

    return join_token