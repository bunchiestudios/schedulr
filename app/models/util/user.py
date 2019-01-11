from app import db

from app.models import User

def get_or_create_user(*, name: str, email: str) -> User:
    session = db.get_session()
    user = session.query(User).filter(User.email == email).one_or_none()
    if user:
        return user
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    return user