import time

from flask import g, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import User, Token

def get_engine():
    return current_app.db_engine

def get_session() -> Session:
    if 'db_session' not in g:
        g.db_session = current_app.db_Session()
    return g.db_session

def get_or_create_user(*, name: str, email: str) -> int:
    session = get_session()
    user = session.query(User).filter(User.email == email).one_or_none()
    if user:
        return user.id

    session.add(User(name=name, email=email))
    session.commit()
    user = session.query(User).filter(User.email == email).one_or_none()
    return user.id

def save_token(*, user_id: int, token: str) -> bool:
    session = get_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()

    # If user does not exist, do not save token and return False as error
    if not user:
        return False

    session.add(Token(token_str=token, time_created=int(time.time()), user=user))
    session.commit()
    return True
