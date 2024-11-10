import os
from dotenv import load_dotenv
from flask_oauthlib.client import OAuth
from models import OAuthToken
# Load environment variables from .env file
load_dotenv()

# OAuth provider client credentials
OAUTH_PROVIDERS = {
    "google": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "authorization_base_url": "https://accounts.google.com/o/oauth2/auth",
        "token_url": "https://accounts.google.com/o/oauth2/token",
        "authorize_url":"https://accounts.google.com/o/oauth2/auth",
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
    },
    "wc": {
        "client_id": os.getenv("WC_CLIENT_ID"),
        "client_secret": os.getenv("WC_CLIENT_SECRET"),
        "authorization_endpoint": f"{os.getenv('WC_PROVIDER_INSTANCE')}oauth2/auth",
        "token_endpoint": f"{os.getenv('WC_PROVIDER_INSTANCE')}oauth2/token",
        "issuer": os.getenv('WC_PROVIDER_INSTANCE'),
        "redirect_uri": os.getenv("WC_REDIRECT_URI"),

    },
    "github": {
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
        "authorization_base_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"),
    },
    "microsoft": {
        "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
        "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET"),
        "authorization_base_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "redirect_uri": os.getenv("MICROSOFT_REDIRECT_URI"),
    },
}

class OAuthIntegration:
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.client_id = OAUTH_PROVIDERS[provider_name]["client_id"]
        self.client_secret = OAUTH_PROVIDERS[provider_name]["client_secret"]
        self.authorization_base_url = OAUTH_PROVIDERS[provider_name].get("authorization_base_url", "")
        self.token_url = OAUTH_PROVIDERS[provider_name].get("token_url", "")
        self.authorize_url = OAUTH_PROVIDERS[provider_name].get("authorize_url", "")
        self.redirect_uri = OAUTH_PROVIDERS[provider_name]["redirect_uri"]
        self.issuer = OAUTH_PROVIDERS[provider_name].get("issuer", "")

    def get_oauth_session(self, app):
        """
        Create and return an OAuth session object for the provider.
        """
        oauth = OAuth(app)
        oauth_session = oauth.remote_app(
            self.provider_name,
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            request_token_params={"scope": "openid profile email"},
            base_url=self.authorization_base_url,
            request_token_url=None,
            access_token_method="POST",
            access_token_url=self.token_url,
            authorize_url=self.authorization_base_url,
        )
        return oauth_session

    def get_oauth_token(self, app, authorization_response):
        """
        Fetch OAuth token for the provider using the authorization response.
        """
        oauth_session = self.get_oauth_session(app)
        response = oauth_session.authorized_response(authorization_response)
        if response is None or response.get("access_token") is None:
            raise ValueError("Invalid OAuth response")
        token = response
        return OAuthToken(access_token=token['access_token'], token_type=token['token_type'], expires_in=token['expires_in'])

    def get_user_info_url(self, provider):
        if provider == "google":
            return "https://www.googleapis.com/oauth2/v1/userinfo"
        elif provider == "wc":
            return self.issuer
        elif provider == "github":
            return "https://api.github.com/user"
        elif provider == "microsoft":
            return "https://graph.microsoft.com/v1.0/me"
        return None

