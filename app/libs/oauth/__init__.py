import urllib.parse as urlparse
import requests


class OauthProvider:
    def __init__(self, client_id, client_secret, scope, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.response_type = None
        self.response_mode = None
        self.url_auth = None
        self.url_token = None

    def get_authorization_url(self):
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "response_mode": self.response_mode,
            "scope": self.scope,
        }
        return self.url_auth + "?" + urlparse.urlencode(params)

    def request_token(self, *, code):
        r = requests.post(
            self.url_token,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            },
        )
        r.raise_for_status()
        return r.json()["access_token"]


class MsftOauth(OauthProvider):
    def __init__(self, *, client_id, client_secret, scope, redirect_uri):
        super(MsftOauth, self).__init__(client_id, client_secret, scope, redirect_uri)
        self.response_type = "code"
        self.response_mode = "query"
        self.url_auth = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
        self.url_token = "https://login.microsoftonline.com/common/oauth2/v2.0/token"


class GoogleOauth(OauthProvider):
    def __init__(self, *, client_id, client_secret, scope, redirect_uri):
        super(GoogleOauth, self).__init__(client_id, client_secret, scope, redirect_uri)
        self.response_type = "code"
        self.response_mode = "query"
        self.url_auth = "https://accounts.google.com/o/oauth2/v2/auth"
        self.url_token = "https://www.googleapis.com/oauth2/v4/token"
