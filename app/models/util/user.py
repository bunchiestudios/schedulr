from app import db

from app.models import User

def get_or_create_user(*, name: str, email: str) -> int:
    session = db.get_session()
    user = session.query(User).filter(User.email == email).one_or_none()
    if user:
        return user.id

    session.add(User(name=name, email=email))
    session.commit()
    user = session.query(User).filter(User.email == email).one_or_none()
    return user.id