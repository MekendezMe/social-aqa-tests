from clients.base_client import BaseClient


class UsersClient(BaseClient):
    ME_URL = '/users/me'
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.base_url = base_url

    def get_me(self):
        response = self.get(endpoint=self.ME_URL)
        return response