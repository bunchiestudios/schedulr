from datetime import datetime

from app import db

from app.models import Token, User

def save_token(*, user_id: int, token: str) -> bool:
    session = db.get_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()

    # If user does not exist, do not save token and return False as error
    if not user:
        return False

    session.add(Token(token_str=token, time_created=datetime.utcnow(), user=user))
    session.commit()
    return True