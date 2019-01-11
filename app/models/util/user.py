from app import db

from app.models import User, Token

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