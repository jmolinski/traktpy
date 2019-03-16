from __future__ import annotations

import urllib.parse
from typing import Any, Dict

import requests
from trakt.core.abstract import AbstractComponent


class DefaultHttpComponent(AbstractComponent):
    name = "http"

    def request(
        self,
        path: str,
        *,
        method: str = "GET",
        query_args: Dict[str, str] = None,
        data: Any = None,
        **kwargs: Any
    ) -> Any:

        url = urllib.parse.urljoin(self.client.config["http"]["base_url"], path)

        query_args = query_args or {}
        data = data or {}

        response = requests.request(
            method, url, params=query_args, data=data, headers=self.get_headers()
        )
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

    def get_url(self, path: str, query_args: Dict[str, str] = None) -> str:
        query_args = query_args or {}

        url_parts = list(urllib.parse.urlparse(self.client.config["http"]["base_url"]))
        url_parts[2] = path
        url_parts[4] = urllib.parse.urlencode(query_args or {})

        return urllib.parse.urlunparse(url_parts)
