from pydantic import BaseModel
from typing import Optional


class OAuthToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class OAuthProvider(BaseModel):
    provider_name: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[int] = None
