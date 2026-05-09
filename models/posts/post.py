from typing import List, Optional

from pydantic import BaseModel

from models.auth.user import User


class Post(BaseModel):
    post_id: int
    content: str
    created_at: str
    comments_count: int
    liked_by_user: bool
    likes_count: int
    media: Optional[List[str]]
    subscribed_by_user: bool
    user: User