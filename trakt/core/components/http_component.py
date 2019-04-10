from __future__ import annotations

import json
import urllib.parse
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Optional

import requests
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

if TYPE_CHECKING:  # pragma: no cover
    from trakt.api import TraktApi

STATUS_CODE_MAPPING = {
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


class DefaultHttpComponent:
    name = "http"
    client: TraktApi
    _requests = requests
    _last_response: Any

    def __init__(self, client: TraktApi, requests_dependency: Any = None) -> None:
        self.client = client
        self._requests = requests_dependency if requests_dependency else requests

    def request(
        self,
        path: str,
        *,
        method: str = "GET",
        query_args: Dict[str, str] = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        no_raise: bool = False,
        use_cache: bool = False,
        **kwargs: Any,
    ) -> ApiResponse:

        url = urllib.parse.urljoin(self.client.config["http"]["base_url"], path)

        query_args = query_args or {}
        data = json.dumps(data or {})

        headers = {
            "Content-type": "application/json",
            **(headers if headers is not None else self.get_headers()),
        }  # {} disables get_headers call

        if use_cache and self.client.cache.has(url, query_args, headers):
            response = self.client.cache.get(url, query_args, headers)
        else:
            response = self._requests.request(
                method, url, params=query_args, data=data, headers=headers
            )

        self._last_response = response

        if not no_raise:
            self._handle_code(response)

        json_response = self._get_json(response, no_raise=no_raise)
        return ApiResponse(
            json_response, response, self._get_pagination_headers(response)
        )

    @staticmethod
    def _get_json(response: Any, no_raise: bool) -> Any:
        try:
            return response.json()
        except BaseException:  # pragma: no cover
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

    @staticmethod
    def _handle_code(response: Any) -> None:
        code = response.status_code

        if code in STATUS_CODE_MAPPING:
            raise STATUS_CODE_MAPPING[code](code, response=response)

        if code // 100 in {4, 5}:
            raise RequestRelatedError(code=code, response=response)

    def get_url(self, path: str, query_args: Dict[str, str] = None) -> str:
        query_args = query_args or {}

        url_parts = list(urllib.parse.urlparse(self.client.config["http"]["base_url"]))
        url_parts[2] = path
        url_parts[4] = urllib.parse.urlencode(query_args or {})

        return urllib.parse.urlunparse(url_parts)

    @staticmethod
    def _get_pagination_headers(response: Any) -> Dict[str, str]:
        headers = response.headers

        return {
            "item_count": headers.get("X-Pagination-Item-Count"),
            "limit": headers.get("X-Pagination-Limit"),
            "page": headers.get("X-Pagination-Page"),
            "page_count": headers.get("X-Pagination-Page-Count"),
        }

    def cache_last_request(self) -> None:
        pass


@dataclass
class ApiResponse:
    json: Any
    original: Any
    pagination: Any = None
