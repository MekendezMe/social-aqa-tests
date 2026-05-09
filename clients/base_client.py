import requests
from pydantic import BaseModel
from requests import Response


class BaseClient:
    DEFAULT_TIMEOUT = 10
    DEFAULT_HEADERS = {"Accept": "application/json"}
    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def post(self, endpoint: str, payload: BaseModel | dict | None = None, headers: dict | None = None) -> Response:
        json_payload = self._prepare_data(payload)
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        response = self.session.post(url=url, json=json_payload,
                                     headers=headers,
                                     timeout=self.timeout)
        return response

    def post_form_data(
            self,
            endpoint: str,
            data: dict | None = None,
            files: dict | None = None,
            headers: dict | None = None,
    ):
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        response = self.session.post(url=url, data=data, files=files,
                                     headers=headers,
                                     timeout=self.timeout)
        return response

    def get(self, endpoint: str, query_params: BaseModel | dict | None = None, headers: dict | None = None) -> Response:
        parsed_query_params = self._prepare_data(query_params)
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        response = self.session.get(url=url, params=parsed_query_params,
                                     headers=headers,
                                     timeout=self.timeout)
        return response

    def delete(self, endpoint: str, payload: BaseModel | dict | None = None, headers: dict | None = None) -> Response:
        json_payload = self._prepare_data(payload)
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        response = self.session.delete(url=url, json=json_payload,
                                     headers=headers,
                                     timeout=self.timeout)
        return response

    def _build_url(self, endpoint: str) -> str:
        return f'{self.base_url}{endpoint}'

    def set_headers(self, headers: dict) -> None:
        self.session.headers.update(headers)

    @staticmethod
    def _prepare_data(data: BaseModel | dict | None) -> dict | None:
        return data.model_dump() if isinstance(data, BaseModel) else data

    def _merge_headers(self, headers: dict | None = None) -> dict:
        return {
            **self.DEFAULT_HEADERS,
            **(headers or {}),
        }