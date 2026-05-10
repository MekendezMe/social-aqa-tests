import json

import allure
import requests
from pydantic import BaseModel
from requests import Response

from utils.logger import get_logger


class BaseClient:
    DEFAULT_TIMEOUT = 10
    DEFAULT_HEADERS = {"Accept": "application/json"}
    logger = get_logger(__name__)
    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def post(self, endpoint: str, payload: BaseModel | dict | None = None, headers: dict | None = None) -> Response:
        json_payload = self._prepare_data(payload)
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        with allure.step(f"POST {endpoint}"):
            self.logger.info(
                "REQUEST: %s %s\n\nHeaders:\n %s\n\nPayload:\n %s", "POST",
                url, self._sanitize(headers),self._sanitize(json_payload))
            response = self.session.post(url=url, json=json_payload,
                                     headers=headers,
                                     timeout=self.timeout)
            self.logger.info(
                "RESPONSE: %s %s -> %s\nBody:\n %s",
                "POST",
                url,
                response.status_code, response.text
            )

            self._attach_http_exchange(
                method="POST",
                url=url,
                request_data=json_payload,
                response=response,
            )
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
        with allure.step(f"POST-form-data {endpoint}"):
            self.logger.info(
                "REQUEST: %s %s\n\nHeaders:\n%s\n\nData:\n%s\n\nFiles:\n%s",
                "POST FORM-DATA",
                url,
                self._sanitize(headers),
                self._sanitize(data),
                list(files.keys()) if files else None,
            )
            response = self.session.post(url=url, data=data, files=files,
                                     headers=headers,
                                     timeout=self.timeout)
            self.logger.info(
                "RESPONSE: %s %s -> %s\n\nBody:\n%s",
                "POST FORM-DATA",
                url,
                response.status_code,
                response.text,
            )
            self._attach_http_exchange(
                method="POST-form-data",
                url=url,
                request_data=files,
                response=response,
            )
            return response

    def get(self, endpoint: str, query_params: BaseModel | dict | None = None, headers: dict | None = None) -> Response:
        parsed_query_params = self._prepare_data(query_params)
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        with allure.step(f"GET {endpoint}"):
            self.logger.info(
                "REQUEST: %s %s\n\nHeaders:\n%s\n\nQuery params:\n%s",
                "GET",
                url,
                self._sanitize(headers),
                self._sanitize(parsed_query_params),
            )
            response = self.session.get(url=url, params=parsed_query_params,
                                     headers=headers,
                                     timeout=self.timeout)

            self.logger.info(
                "RESPONSE: %s %s -> %s\n\nBody:\n%s",
                "GET",
                url,
                response.status_code,
                response.text,
            )
            self._attach_http_exchange(
                method="GET",
                url=url,
                request_data=parsed_query_params,
                response=response,
            )
            return response

    def delete(self, endpoint: str, payload: BaseModel | dict | None = None, headers: dict | None = None) -> Response:
        json_payload = self._prepare_data(payload)
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        with allure.step(f"DELETE {endpoint}"):
            self.logger.info(
                "REQUEST: %s %s\n\nHeaders:\n%s\n\nPayload:\n%s",
                "DELETE",
                url,
                self._sanitize(headers),
                self._sanitize(json_payload),
            )
            response = self.session.delete(url=url, json=json_payload,
                                     headers=headers,
                                     timeout=self.timeout)
            self.logger.info(
                "RESPONSE: %s %s -> %s\n\nBody:\n%s",
                "DELETE",
                url,
                response.status_code,
                response.text,
            )
            self._attach_http_exchange(
                method="DELETE",
                url=url,
                request_data=json_payload,
                response=response,
            )
            return response

    def patch(self, endpoint: str, payload: BaseModel | dict | None = None, headers: dict | None = None) -> Response:
        json_payload = self._prepare_data(payload)
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        with allure.step(f"PATCH {endpoint}"):
            self.logger.info(
                "REQUEST: %s %s\n\nHeaders:\n%s\n\nPayload:\n%s",
                "PATCH",
                url,
                self._sanitize(headers),
                self._sanitize(json_payload),
            )
            response = self.session.patch(url=url, json=json_payload,
                                     headers=headers,
                                     timeout=self.timeout)
            self.logger.info(
                "RESPONSE: %s %s -> %s\n\nBody:\n%s",
                "PATCH",
                url,
                response.status_code,
                response.text,
            )
            self._attach_http_exchange(
                method="PATCH",
                url=url,
                request_data=json_payload,
                response=response,
            )
            return response

    def patch_form_data(
            self,
            endpoint: str,
            data: dict | None = None,
            files: dict | None = None,
            headers: dict | None = None,
    ):
        headers = self._merge_headers(headers)
        url = self._build_url(endpoint)
        with allure.step(f"PATCH-form-data {endpoint}"):
            self.logger.info(
                "REQUEST: %s %s\n\nHeaders:\n%s\n\nData:\n%s\n\nFiles:\n%s",
                "PATCH FORM-DATA",
                url,
                self._sanitize(headers),
                self._sanitize(data),
                list(files.keys()) if files else None,
            )
            response = self.session.patch(url=url, data=data, files=files,
                                     headers=headers,
                                     timeout=self.timeout)
            self.logger.info(
                "RESPONSE: %s %s -> %s\n\nBody:\n%s",
                "PATCH FORM-DATA",
                url,
                response.status_code,
                response.text,
            )
            self._attach_http_exchange(
                method="PATCH-form-data",
                url=url,
                request_data=files,
                response=response,
            )
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

    @staticmethod
    def _attach_json(name: str, data) -> None:
        if data is None:
            return

        allure.attach(
            json.dumps(data, indent=2, ensure_ascii=False),
            name=name,
            attachment_type=allure.attachment_type.JSON,
        )

    @staticmethod
    def _attach_http_exchange(method: str, url: str, request_data, response: Response) -> None:
        data = {
            "request": {
                "method": method,
                "url": url,
                "body": request_data,
            },
            "response": {
                "status_code": response.status_code,
                "body": response.text,
            },
        }

        allure.attach(
            json.dumps(data, indent=2, ensure_ascii=False),
            name=f"{method} {url}",
            attachment_type=allure.attachment_type.JSON,
        )



    @staticmethod
    def _sanitize(data):
        if data is None:
            return None
        sensitive_fields = {"password", "access_token", "refresh_token", "authorization"}

        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if key.lower() in sensitive_fields:
                    sanitized[key] = "***"
                else:
                    sanitized[key] = value
            return sanitized

        return data