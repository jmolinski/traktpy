import json
from collections import defaultdict
from typing import Any, Dict, Tuple

from trakt.core.components.http_component import DefaultHttpComponent

try:
    with open(".secrets") as f:
        config = json.loads(f.read())
except:  # NOQA
    config = {"client_secret": "", "client_id": ""}


class MockResponse:
    def __init__(self, json_response, code):
        self.status_code = code
        self.json_response = json_response

    def json(self):
        return self.json_response


class MockRequests:
    def __init__(self, map_of_responses):
        self.m = {}
        self.req_map = defaultdict(list)
        self.fixed_response = False

        if "*" in map_of_responses:
            self.response = MockResponse(*map_of_responses["*"])
            self.fixed_response = True
        else:
            for path, (json_response, code) in map_of_responses.items():
                self.m[path] = MockResponse(json_response, code)

    def request(self, method, path, *args, **kwargs):
        p = path.split(".tv/")[1]

        # log request
        self.req_map[p].append(
            {**kwargs, "method": method, "path": path, "resource": p}
        )

        if self.fixed_response:
            return self.response

        return self.m[p]


def get_mock_http_component(map_of_responses: Dict[str, Tuple[Any, int]]):
    # '*' key in map is wildcard

    def wrapper(client):
        return DefaultHttpComponent(
            client, requests_dependency=MockRequests(map_of_responses)
        )

    return wrapper
