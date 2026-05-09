from http import HTTPStatus

import pytest

from clients.posts_client import PostsClient
from config.settings import BASE_URL
from models.posts.requests import GetAllPostsRequest, CreatePostRequest, DeletePostRequest
from models.posts.responses import CreatePostResponse
from test_data.generators import post_generator

DEFAULT_LIMIT_POSTS = 50
DEFAULT_PAGE = 1
DEFAULT_TYPE = 'all'

LIMIT_FOR_CHECK = 1

@pytest.fixture
def posts_client(authenticated_user) -> PostsClient:
    client = PostsClient(base_url=BASE_URL)
    client.set_headers(headers={"Authorization": f"Bearer {authenticated_user.access_token}",
        "Device-ID": authenticated_user.device_id})
    return client

@pytest.fixture
def posts_client_unauthorized() -> PostsClient:
    client = PostsClient(base_url=BASE_URL)
    return client

@pytest.fixture
def generated_default_get_all_posts_params():
    return GetAllPostsRequest(page_number=DEFAULT_PAGE, limit=DEFAULT_LIMIT_POSTS, type=DEFAULT_TYPE)

@pytest.fixture
def generated_params_with_limit():
    return GetAllPostsRequest(page_number=DEFAULT_PAGE, limit=LIMIT_FOR_CHECK, type=DEFAULT_TYPE)

@pytest.fixture
def generated_content_for_post():
    return post_generator.generate_post()

@pytest.fixture
def created_post(posts_client, generated_content_for_post):
    response = posts_client.create_post(generated_content_for_post)
    assert response.status_code == HTTPStatus.CREATED
    created_post = CreatePostResponse(**response.json())

    yield created_post

    delete_response = posts_client.delete_post(DeletePostRequest(id=created_post.post_id))
    assert delete_response.status_code == HTTPStatus.OK