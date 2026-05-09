from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]