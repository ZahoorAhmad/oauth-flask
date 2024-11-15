from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel

# from . import OAuthIntegration
from .app import db

load_dotenv()


class OAuthToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class OAuthProvider(BaseModel):
    provider_name: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[int] = None


class CommonModel:
    def save(self):
        """Save the token to the database."""
        db.session.add(self)
        db.session.commit()


# Token model
class Token(CommonModel):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    access_token = db.Column(db.String(200), nullable=False)
    refresh_token = db.Column(db.String(200), nullable=True)
    expires_in = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<Token {self.provider}>"

    def is_expired(self):
        """Check if the token is expired."""
        return datetime.utcnow() > self.created_at + timedelta(seconds=self.expires_in)

    def save(self):
        """Save the token to the database."""
        db.session.add(self)
        db.session.commit()

    def refresh(self):
        """Refresh the token."""
        # Assuming `OAuthIntegration` can handle refreshing the token
        from . import OAuthIntegration
        oauth_integration = OAuthIntegration(self.provider)
        refreshed_token = oauth_integration.refresh_token(self.refresh_token)
        self.access_token = refreshed_token.access_token
        self.refresh_token = refreshed_token.refresh_token
        self.expires_in = refreshed_token.expires_in
        self.created_at = datetime.now()
        db.session.commit()


# User model
class User(CommonModel):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    token_id = db.Column(db.Integer, db.ForeignKey('token.id'), nullable=False)
    token = db.relationship('Token', backref=db.backref('user', uselist=False))

    def __repr__(self):
        return f"<User {self.username}>"
