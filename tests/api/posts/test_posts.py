from http import HTTPStatus

import pytest

from models.error import ErrorResponse
from models.posts.requests import GetAllPostsRequest, GetPostRequest
from models.posts.responses import GetAllPostsResponse, CreatePostResponse, GetPostResponse


@pytest.mark.smoke
@pytest.mark.posts
def test_successful_get_all_posts(posts_client, generated_default_get_all_posts_params):
    response = posts_client.get_posts(query_params=generated_default_get_all_posts_params)
    assert response.status_code == HTTPStatus.OK
    parsed_response = GetAllPostsResponse(**response.json())
    assert len(parsed_response.posts) > 0

@pytest.mark.posts
@pytest.mark.regression
def test_get_all_posts_with_limit(posts_client, generated_params_with_limit):
    response = posts_client.get_posts(query_params=generated_params_with_limit)
    assert response.status_code == HTTPStatus.OK
    parsed_response = GetAllPostsResponse(**response.json())
    assert len(parsed_response.posts) == 1

@pytest.mark.posts
@pytest.mark.regression
@pytest.mark.negative
def test_get_all_posts_unauthorized(posts_client_unauthorized, generated_default_get_all_posts_params):
    response = posts_client_unauthorized.get_posts(query_params=generated_default_get_all_posts_params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    error_response = ErrorResponse(**response.json())
    assert 'missing' in error_response.error.lower()

@pytest.mark.posts
@pytest.mark.regression
def test_different_pages_return_different_posts(posts_client):
    query_params_first_page = GetAllPostsRequest(page_number=1, limit=1)
    query_params_second_page = GetAllPostsRequest(page_number=2, limit=1)
    first_page_response = posts_client.get_posts(query_params=query_params_first_page)
    second_page_response = posts_client.get_posts(query_params=query_params_second_page)
    assert first_page_response.status_code == HTTPStatus.OK
    assert second_page_response.status_code == HTTPStatus.OK
    first_page_parsed_response = GetAllPostsResponse(**first_page_response.json())
    second_page_parsed_response = GetAllPostsResponse(**second_page_response.json())
    assert len(first_page_parsed_response.posts) > 0
    assert len(second_page_parsed_response.posts) > 0
    assert first_page_parsed_response.posts[0].post_id != second_page_parsed_response.posts[0].post_id

@pytest.mark.posts
@pytest.mark.smoke
def test_user_can_get_created_post_by_id(posts_client, created_post):
    post_id = created_post.post_id
    assert post_id > 0
    post = posts_client.get_post(data=GetPostRequest(id=post_id))
    assert post.status_code == HTTPStatus.OK
    parsed_post = GetPostResponse(**post.json())
    assert parsed_post.post_id == post_id
    assert parsed_post.content == created_post.content

