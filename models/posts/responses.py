from typing import List

from pydantic import BaseModel

from models.posts.post import Post


class GetAllPostsResponse(BaseModel):
    posts: List[Post]
    last_page: bool

class GetPostResponse(Post):
    pass

class CreatePostResponse(Post):
    pass

class DeletePostResponse(BaseModel):
    success: bool