from typing import Optional

from app import db
from app.models import Project, Team


def get_project_by_id(id: int) -> Optional[Project]:
    """
    Return a project given the ID (database unique key).

    :param id: The ID to search with.
    :return: Returns Project with given ID, or None if it does not exist.
    """
    session = db.get_session()
    return session.query(Project).filter(Project.id == id).one_or_none()


def add_project(name: str, team_id: int) -> Optional[Project]:
    """
    Adds a project into the DB and returns that same project.

    :param name: Human-readable name of the project
    :param team_id: The ID of the team this project is assigned to.
    :return: The created project, or none if there was an issue.
    """
    session = db.get_session()
    team = session.query(Team).filter(Team.id == team_id).one_or_none()

    if not team:
        return None

    project = Project(name=name, team=team)
    session.add(project)
    session.commit()

    return project
