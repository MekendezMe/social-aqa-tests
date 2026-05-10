import requests
from requests import Response

from clients.base_client import BaseClient
from models.auth.requests import RegisterRequest, LoginRequest


class AuthClient(BaseClient):
    REGISTER_URL = '/auth/signup'
    LOGIN_URL = '/auth/login'
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.base_url = base_url

    def register(self, payload: RegisterRequest) -> Response:
        response = self.post(endpoint=self.REGISTER_URL, payload=payload)
        return response

    def login(self, payload: LoginRequest) -> Response:
        response = self.post(endpoint=self.LOGIN_URL, payload=payload)
        return response