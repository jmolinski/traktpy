import urllib.parse
from typing import Any, Dict

import requests
from trakt.core.abstract import AbstractApi, AbstractComponent
from trakt.core.exceptions import (
    BadRequest,
    Conflict,
    Forbidden,
    MethodNotFound,
    NotFound,
    PreconditionFailed,
    RateLimitExceeded,
    ServerError,
    ServiceUnavailable,
    Unauthorized,
    UnprocessableEntity,
)


class DefaultHttpComponent(AbstractComponent):
    name = "http"
    _requests = requests

    def __init__(self, client: AbstractApi, requests_dependency: Any = None) -> None:
        super().__init__(client)

        self._requests = requests_dependency if requests_dependency else requests

    def request(
        self,
        path: str,
        *,
        method: str = "GET",
        query_args: Dict[str, Any] = None,
        data: Any = None,
        **kwargs: Any,
    ) -> Any:

        url = urllib.parse.urljoin(self.client.config["http"]["base_url"], path)

        query_args = query_args or {}
        data = data or {}

        response = self._requests.request(
            method, url, params=query_args, data=data, headers=self.get_headers()
        )

        self.handle_code(response.status_code)

        return response.json()

    def get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-type": "application/json",
            "trakt-api-key": self.client.client_id,
            "trakt-api-version": 2,
        }

        if self.client.authenticated:
            headers["Authorization"] = self.client.oauth.token

        str_headers = {k: str(v) for k, v in headers.items()}

        return str_headers

    def handle_code(self, code: int) -> None:
        m = {
            400: BadRequest,
            401: Unauthorized,
            403: Forbidden,
            404: NotFound,
            405: MethodNotFound,
            409: Conflict,
            412: PreconditionFailed,
            422: UnprocessableEntity,
            429: RateLimitExceeded,
            500: ServerError,
            503: ServiceUnavailable,
            504: ServiceUnavailable,
            520: ServiceUnavailable,
            521: ServiceUnavailable,
            522: ServiceUnavailable,
        }

        if code in m:
            raise m[code](code)
