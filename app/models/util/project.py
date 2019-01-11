from typing import Optional

from app import db
from app.models import Project

def get_project_by_id(id: int) -> Optional[Project]:
    """
    Return a project given the ID (database unique key).

    :param id: The ID to search with.
    :return: Returns Project with given ID, or None if it does not exist.
    """
    session = db.get_session()
    return session.query(Project).filter(Project.id == id).one_or_none()
