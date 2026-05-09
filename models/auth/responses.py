from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    device_id: str
    refresh_token: str