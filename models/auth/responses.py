from pydantic import BaseModel

from models.auth.user import User


class TokenResponse(BaseModel):
    access_token: str
    device_id: str
    refresh_token: str


class UserResponse(User):
    pass