from __future__ import annotations

import json
import urllib.parse
from typing import Any, Dict, Optional

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
    RequestRelatedError,
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
        query_args: Dict[str, str] = None,
        data: Any = None,
        return_code: bool = False,
        headers: Optional[Dict[str, str]] = None,
        no_raise: bool = False,
        **kwargs: Any,
    ) -> Any:

        url = urllib.parse.urljoin(self.client.config["http"]["base_url"], path)

        query_args = query_args or {}
        data = json.dumps(data or {})

        headers = {
            "Content-type": "application/json",
            **(headers if headers is not None else self.get_headers()),
        }  # {} disables get_headers call

        response = self._requests.request(
            method, url, params=query_args, data=data, headers=headers
        )

        if not no_raise:
            self.handle_code(response)

        json_response = self._get_json(response, no_raise=no_raise)

        if return_code:
            return json_response, response.status_code

        return json_response

    def _get_json(self, response: Any, no_raise: bool) -> Any:
        try:
            return response.json()
        except:  # NOQA
            if no_raise:
                return {}
            else:
                raise

    def get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "trakt-api-key": self.client.client_id,
            "trakt-api-version": 2,
        }

        if self.client.user:
            headers["Authorization"] = self.client.user.access_token

        str_headers = {k: str(v) for k, v in headers.items()}

        return str_headers

    def handle_code(self, response: Any) -> None:
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

        code = response.status_code

        if code in m:
            raise m[code](code, response=response)

        if code // 100 in {4, 5}:
            raise RequestRelatedError(code=code, response=response)

    def get_url(self, path: str, query_args: Dict[str, str] = None) -> str:
        query_args = query_args or {}

        url_parts = list(urllib.parse.urlparse(self.client.config["http"]["base_url"]))
        url_parts[2] = path
        url_parts[4] = urllib.parse.urlencode(query_args or {})

        return urllib.parse.urlunparse(url_parts)
