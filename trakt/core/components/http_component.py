from typing import Any, Dict, cast

import requests
from trakt.core.abstract import AbstractComponent


class HttpComponent(AbstractComponent):
    name = "http"

    def request(
        self, method, path, headers=None, data=None, *args, **kwargs
    ) -> Dict[str, Any]:
        url = self.resolve_path(path)
        response = requests.get(url)
        return response.json()

    def resolve_path(self, *args):
        return ""
