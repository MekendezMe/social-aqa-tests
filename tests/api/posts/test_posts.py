from http import HTTPStatus

import allure
import pytest

from models.error import ErrorResponse
from models.posts.requests import GetAllPostsRequest, GetPostRequest, UpdatePostRequest, DeletePostRequest, \
    CreatePostRequest
from models.posts.responses import GetAllPostsResponse, CreatePostResponse, GetPostResponse, UpdatePostResponse
from models.success import SuccessResponse


pytestmark = [
    allure.feature("Posts"),
    pytest.mark.posts,
]


@pytest.mark.smoke
def test_successful_get_all_posts(posts_client, generated_default_get_all_posts_params):
    response = posts_client.get_posts(query_params=generated_default_get_all_posts_params)
    assert response.status_code == HTTPStatus.OK
    parsed_response = GetAllPostsResponse(**response.json())
    assert len(parsed_response.posts) > 0

@pytest.mark.regression
def test_get_all_posts_with_limit(posts_client, generated_params_with_limit):
    response = posts_client.get_posts(query_params=generated_params_with_limit)
    assert response.status_code == HTTPStatus.OK
    parsed_response = GetAllPostsResponse(**response.json())
    assert len(parsed_response.posts) == 1

@pytest.mark.smoke
@pytest.mark.negative
def test_get_all_posts_unauthorized(posts_client_unauthorized, generated_default_get_all_posts_params):
    response = posts_client_unauthorized.get_posts(query_params=generated_default_get_all_posts_params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    error_response = ErrorResponse(**response.json())
    assert 'missing' in error_response.error.lower()

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

@pytest.mark.smoke
def test_user_can_get_created_post_by_id(posts_client, created_post):
    post_id = created_post.post_id
    assert post_id > 0
    post = posts_client.get_post(data=GetPostRequest(id=post_id))
    assert post.status_code == HTTPStatus.OK
    parsed_post = GetPostResponse(**post.json())
    assert parsed_post.post_id == post_id
    assert parsed_post.content == created_post.content


@pytest.mark.regression
@pytest.mark.negative
def test_get_non_existing_post(posts_client):
    post_id = -1
    post = posts_client.get_post(data=GetPostRequest(id=post_id))
    assert post.status_code == HTTPStatus.BAD_REQUEST
    error_response = ErrorResponse(**post.json())
    assert 'record not found' in error_response.error.lower()

@pytest.mark.smoke
def test_create_post(created_post):
    assert created_post.post_id > 0

@pytest.mark.smoke
def test_update_own_post(posts_client, created_post, create_content_for_post):
    generated_content = create_content_for_post()
    assert created_post.post_id > 0
    response = posts_client.update_post(UpdatePostRequest(id=created_post.post_id,
                                                          content=generated_content.content))
    assert response.status_code == HTTPStatus.OK, response.text
    parsed_response = UpdatePostResponse(**response.json())
    assert parsed_response.post_id == created_post.post_id
    assert parsed_response.content != created_post.content

@pytest.mark.negative
@pytest.mark.regression
def test_update_not_own_post(posts_client, second_posts_client, created_post, create_content_for_post):
    generated_content = create_content_for_post()
    assert created_post.post_id > 0
    response = second_posts_client.update_post(UpdatePostRequest(id=created_post.post_id,
                                                          content=generated_content.content))
    assert response.status_code == HTTPStatus.NOT_FOUND
    error_response = ErrorResponse(**response.json())
    assert 'not found' in error_response.error.lower()

@pytest.mark.smoke
def test_delete_own_post(posts_client, created_post):
    assert created_post.post_id > 0
    response = posts_client.delete_post(DeletePostRequest(id=created_post.post_id))
    assert response.status_code == HTTPStatus.OK, response.text
    parsed_response = SuccessResponse(**response.json())
    assert parsed_response.success
    post = posts_client.get_post(GetPostRequest(id=created_post.post_id))
    assert post.status_code == HTTPStatus.BAD_REQUEST
    error_response = ErrorResponse(**post.json())
    assert 'record not found' in error_response.error.lower()


@pytest.mark.negative
@pytest.mark.regression
def test_delete_not_own_post(posts_client, second_posts_client, created_post):
    assert created_post.post_id > 0
    response = second_posts_client.delete_post(DeletePostRequest(id=created_post.post_id))
    assert response.status_code == HTTPStatus.OK, response.text
    parsed_response = SuccessResponse(**response.json())
    assert not parsed_response.success

@pytest.mark.negative
@pytest.mark.regression
def test_create_empty_post(posts_client):
    response = posts_client.create_post(CreatePostRequest(content=None, media_paths=None))
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
    error_response = ErrorResponse(**response.json())
    assert 'invalid' in error_response.error.lower()

