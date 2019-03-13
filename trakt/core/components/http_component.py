import urllib.parse
from typing import Any, Dict

import requests
from trakt.core.abstract import AbstractComponent


class DefaultHttpComponent(AbstractComponent):
    name = "http"

    def request(
        self, path, *, method="GET", query_args=None, data=None, **kwargs
    ) -> Dict[str, Any]:

        url = urllib.parse.urljoin(self.client.config["http"]["base_url"], path)

        query_args = query_args or {}
        data = data or {}

        response = requests.request(
            method, url, params=query_args, data=data, headers=self.get_headers()
        )
        return response.json()

    def get_headers(self):
        headers = {
            "Content-type": "application/json",
            "trakt-api-key": self.client.client_id,
            "trakt-api-version": 2,
        }

        if self.client.authenticated:
            headers["Authorization"] = self.client.oauth.token

        headers = {k: str(v) for k, v in headers.items()}

        return headers
