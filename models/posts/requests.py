from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel


class GetAllPostsRequest(BaseModel):
    page_number: int
    limit: Optional[int] = None
    type: Optional[str] = None

class GetPostRequest(BaseModel):
    id: int

class DeletePostRequest(BaseModel):
    id: int

class CreatePostRequest(BaseModel):
    content: Optional[str] = None
    media_paths: Optional[list[Path]] = None

class UpdatePostRequest(CreatePostRequest):
    id: int