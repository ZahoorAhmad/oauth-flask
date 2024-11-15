import os

import requests
from dotenv import load_dotenv

from app import OAuthToken

load_dotenv()

# OAuth provider client credentials
OAUTH_PROVIDERS = {
    "google": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "discovery_url": os.getenv("GOOGLE_DISCOVERY_URL"),
    },
    "ibm": {
        "client_id": os.getenv("IBM_CLIENT_ID"),
        "client_secret": os.getenv("IBM_CLIENT_SECRET"),
        "redirect_uri": os.getenv("IBM_REDIRECT_URI"),
        "discovery_url": os.getenv("IBM_DISCOVERY_URL"),
    },
    "wc": {
        "client_id": os.getenv("WC_CLIENT_ID"),
        "client_secret": os.getenv("WC_CLIENT_SECRET"),
        "redirect_uri": os.getenv("WC_REDIRECT_URI"),
        "discovery_url": os.getenv("WC_DISCOVERY_URL"),
    },
    "github": {
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"),
        "discovery_url": os.getenv("GITHUB_DISCOVERY_URL"),
    },
    "microsoft": {
        "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
        "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET"),
        "redirect_uri": os.getenv("MICROSOFT_REDIRECT_URI"),
        "discovery_url": os.getenv("MICROSOFT_DISCOVERY_URL"),
    },
}


class OAuthIntegration:
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.client_id = OAUTH_PROVIDERS[provider_name]["client_id"]
        self.client_secret = OAUTH_PROVIDERS[provider_name]["client_secret"]
        self.redirect_uri = OAUTH_PROVIDERS[provider_name]["redirect_uri"]

        # Fetch the OAuth metadata from the discovery URL
        self.discovery_url = OAUTH_PROVIDERS[provider_name]["discovery_url"]
        self.discovery_data = self.get_discovery_data()

        # Use discovery data to set authorization and token URLs dynamically
        self.authorization_base_url = self.discovery_data.get("authorization_endpoint", "")
        self.token_url = self.discovery_data.get("token_endpoint", "")
        self.authorize_url = self.discovery_data.get("authorization_endpoint", "")
        self.issuer = self.discovery_data.get("issuer", "")

    def get_discovery_data(self):
        """
        Fetch the OAuth discovery metadata from the discovery URL.
        """
        response = requests.get(self.discovery_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch discovery document for {self.provider_name}")

        return response.json()

    def get_oauth_session(self, app):
        """
        Create and return an OAuth session object for the provider.
        """
        from flask_oauthlib.client import OAuth
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
        return OAuthToken(access_token=token['access_token'], token_type=token['token_type'],
                          expires_in=token['expires_in'])

    def get_user_info_url(self, provider):
        if provider == "google":
            return "https://www.googleapis.com/oauth2/v1/userinfo"
        elif provider == "wc":
            return f"{self.issuer}/userinfo"
        elif provider == "github":
            return "https://api.github.com/user"
        elif provider == "microsoft":
            return "https://graph.microsoft.com/v1.0/me"
        return None

    def refresh_token(self, refresh_token):
        """Refresh the OAuth token using the refresh token."""

        # Fetch the provider configuration from the environment
        config = OAUTH_PROVIDERS[self.provider_name]

        payload = {
            "grant_type": "refresh_token",
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "refresh_token": refresh_token,
        }

        response = requests.post(self.token_url, data=payload)

        if response.status_code != 200:
            raise Exception(f"Failed to refresh token for {self.provider_name}: {response.text}")

        data = response.json()
        return OAuthToken(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", refresh_token),
            expires_in=data["expires_in"]
        )
