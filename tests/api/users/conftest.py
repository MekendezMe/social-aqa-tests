import pytest

from clients.users_client import UsersClient
from config import settings


@pytest.fixture
def users_client(create_authenticated_user) -> UsersClient:
    authenticated_user = create_authenticated_user()
    client = UsersClient(settings.BASE_URL)
    client.set_headers(headers={"Authorization": f"Bearer {authenticated_user.access_token}",
                                "Device-ID": authenticated_user.device_id})
    return client