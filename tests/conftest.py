from dataclasses import dataclass

import pytest

from clients.auth_client import AuthClient
from config import settings
from models.auth.requests import RegisterRequest
from models.auth.responses import TokenResponse
from test_data.generators import auth_generator

@dataclass
class RegisterContext:
    user: RegisterRequest
    access_token: str
    refresh_token: str
    device_id: str
@dataclass
class AuthContext:
    user: RegisterRequest
    access_token: str
    refresh_token: str
    device_id: str
    headers: dict


@pytest.fixture(scope="session")
def auth_client():
    return AuthClient(base_url=settings.BASE_URL)

@pytest.fixture
def generated_user():
    return auth_generator.generate_register()

@pytest.fixture
def registered_user(auth_client, generated_user) -> RegisterContext:
    response = auth_client.register(payload=generated_user)
    assert response.status_code == 201
    token_response = TokenResponse(**response.json())
    return RegisterContext(user=generated_user, access_token=token_response.access_token,
                           refresh_token=token_response.refresh_token, device_id=token_response.device_id)


@pytest.fixture
def create_authenticated_user(auth_client):
    def _create_user() -> AuthContext:
        user = auth_generator.generate_register()

        response = auth_client.register(payload=user)
        assert response.status_code == 201, response.text

        token_response = TokenResponse(**response.json())

        return AuthContext(
            user=user,
            access_token=token_response.access_token,
            refresh_token=token_response.refresh_token,
            device_id=token_response.device_id,
            headers={
                "Authorization": f"Bearer {token_response.access_token}",
                "Device-ID": token_response.device_id,
            },
        )

    return _create_user

