

from app.libs.oauth import MsftOauth, GoogleOauth
from flask import current_app, url_for

def __get_redirect_uri_msft():
    return url_for('auth.msft_callback', _external=True)

def get_oauth_client_msft() -> MsftOauth:
    return MsftOauth(
        client_id = current_app.config['MSFT_APP_ID'],
        client_secret = current_app.config['MSFT_APP_SECRET'],
        scope = 'openid User.Read',
        redirect_uri = __get_redirect_uri_msft()
    )

def __get_redirect_uri_google():
    return url_for('auth.google_callback', _external=True)

def get_oauth_client_google() -> GoogleOauth:
    return GoogleOauth(
        client_id = current_app.config['GOOGLE_APP_ID'],
        client_secret = current_app.config['GOOGLE_APP_SECRET'],
        scope = 'openid profile email',
        redirect_uri = __get_redirect_uri_google()
    )