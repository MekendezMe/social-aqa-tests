from http import HTTPStatus

import allure
import pytest

from helpers.assert_token_response import assert_token_response
from models.auth.requests import LoginRequest, RegisterRequest
from models.auth.responses import TokenResponse
from models.error import ErrorResponse

pytestmark = [
    allure.feature("Auth"),
    pytest.mark.auth,
]


@pytest.mark.smoke
def test_successful_user_registration(auth_client, generated_user):
    response = auth_client.register(payload=generated_user)
    assert response.status_code == HTTPStatus.CREATED
    token_response = TokenResponse(**response.json())
    assert_token_response(token_response)


@pytest.mark.smoke
def test_successful_login(auth_client, registered_user):
    login_request = LoginRequest(email=registered_user.user.email, password=registered_user.user.password)
    response = auth_client.login(payload=login_request)
    assert response.status_code == HTTPStatus.OK
    token_response = TokenResponse(**response.json())
    assert_token_response(token_response)


def build_invalid_login_request(registered_user, case: str) -> LoginRequest:
    email = registered_user.user.email
    password = registered_user.user.password

    match case:
        case "invalid_password":
            password += "x"
        case "empty_email":
            email = ""
        case "empty_password":
            password = ""

    return LoginRequest(email=email, password=password)

@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize(
    "case",
    ["invalid_password", "empty_email", "empty_password"],
ids=["invalid_password", "empty_email", "empty_password"],
)
def test_login_with_invalid_credentials(auth_client, registered_user, case):
    login_request = build_invalid_login_request(registered_user, case)
    response = auth_client.login(payload=login_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    error_response = ErrorResponse(**response.json())
    assert 'invalid argument' in error_response.error.lower()

@pytest.mark.regression
@pytest.mark.negative
def test_register_with_existing_email(auth_client, generated_user, registered_user):
    register_request = RegisterRequest(email=registered_user.user.email,
                                 password=generated_user.password, username=generated_user.username)

    response = auth_client.register(payload=register_request)
    assert response.status_code == HTTPStatus.CONFLICT
    error_response = ErrorResponse(**response.json())
    assert 'conflict' in error_response.error.lower()


@pytest.mark.regression
@pytest.mark.negative
def test_register_with_existing_username(auth_client, generated_user, registered_user):
    register_request = RegisterRequest(email=generated_user.email,
                                 password=generated_user.password, username=registered_user.user.username)

    response = auth_client.register(payload=register_request)
    assert response.status_code == HTTPStatus.CONFLICT
    error_response = ErrorResponse(**response.json())
    assert 'conflict' in error_response.error.lower()


