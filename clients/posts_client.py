from clients.base_client import BaseClient
from models.posts.requests import GetAllPostsRequest, GetPostRequest, CreatePostRequest, DeletePostRequest


class PostsClient(BaseClient):
    POSTS_URL = '/posts'
    def __init__(self, base_url: str, timeout: int = 10):
        super().__init__(base_url)
        self.base_url = base_url

    def get_posts(self, query_params: GetAllPostsRequest):
        response = self.get(endpoint=self.POSTS_URL, query_params=query_params)
        return response

    def get_post(self, data: GetPostRequest):
        response = self.get(endpoint=f'{self.POSTS_URL}/{data.id}')
        return response

    def create_post(self, body: CreatePostRequest):
        files = {}
        if body.content:
            files['content'] = (None, body.content)

        response = self.post_form_data(endpoint=self.POSTS_URL, files=files)
        return response

    def delete_post(self, body: DeletePostRequest):
        response = self.delete(endpoint=f'{self.POSTS_URL}/{body.id}', payload=body)
        return response