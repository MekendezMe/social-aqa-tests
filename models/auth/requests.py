from typing import Optional

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str
    name: Optional[str] = None
    last_name: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str