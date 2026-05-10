from http import HTTPStatus

import pytest

from models.auth.responses import UserResponse


@pytest.mark.smoke
@pytest.mark.users
def test_get_current_user(users_client):
    response = users_client.get_me()
    assert response.status_code == HTTPStatus.OK
    parsed_response = UserResponse(**response.json())
    assert parsed_response.user_id > 0