from datetime import datetime

from .models import Token, User, db


def save_token(provider, access_token, refresh_token, expires_in):
    """Save a new token or update an existing token."""
    # Check if we already have a token for the provider
    existing_token = Token.query.filter_by(provider=provider).first()
    if existing_token:
        # If token exists, update it
        existing_token.access_token = access_token
        existing_token.refresh_token = refresh_token
        existing_token.expires_in = expires_in
        existing_token.created_at = datetime.now()
    else:
        # Otherwise, create a new token entry
        new_token = Token(
            provider=provider,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            created_at=datetime.now()
        )
        db.session.add(new_token)

    db.session.commit()
    return existing_token or new_token


def get_user_by_provider_and_token(provider, access_token):
    """Get the user associated with a token."""
    user = User.query.join(Token).filter(Token.provider == provider, Token.access_token == access_token).first()
    return user


def refresh_token_if_needed(provider, token):
    """Refresh the token if expired."""
    if token.is_expired():
        token.refresh()
    return token
