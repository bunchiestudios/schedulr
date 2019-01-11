from datetime import datetime, timedelta

from app import db

from app.models import Token, User

def save_token(*, user_id: int, token: str) -> bool:
    session = db.get_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()

    # If user does not exist, do not save token and return False as error
    if not user:
        return False

    session.add(Token(token_str=token, user=user))
    session.commit()
    return True

def verify_token(token_str: str) -> Token:
    """Looks for a token string in the database and returns the instance associated with it from the database.
    If the token was not found returns None.
    
    Arguments:
        token_str {str} -- Token string to verify
    
    Returns:
        Token -- Token 
    """
    token = db.get_session().query(Token).filter(Token.token_str == token_str).one_or_none()
    return token

def older_than(*, token: Token, hours: int) -> bool:
    """Determines whether a tokes is older than a given amount of hours.
    
    Arguments:
        token {Token} -- Token to verify
        hours {int} -- Hours to verify
    
    Returns:
        bool -- Represents whether or not the token is older than the amount of hours given.
    """
    reference_timestamp = datetime.now() - timedelta(hours=hours)
    return token.timestamp <= reference_timestamp

def destroy_token(token: Token) -> None:
    session = db.get_session()
    session.delete(token)
    session.commit()
    


