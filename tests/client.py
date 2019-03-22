import json
import re
from collections import defaultdict
from typing import Any, Dict, Tuple

from trakt.core.components.http_component import DefaultHttpComponent

try:
    with open(".secrets") as f:
        SECRETS = json.loads(f.read())
except:  # NOQA
    SECRETS = {"client_secret": "", "client_id": ""}


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

        for path, (json_response, code) in map_of_responses.items():
            self.m[".*" + path + ".*"] = MockResponse(json_response, code)

    def request(self, method, path, *args, **kwargs):
        p = path.split(".tv/" if ".tv" in path else ".com/")[1]

        # log request
        self.req_map[p].append(
            {**kwargs, "method": method, "path": path, "resource": p}
        )

        return self.m[self.find_path(path)]

    def find_path(self, v):
        paths = set(self.m.keys())
        matching_paths = [p for p in paths if re.match(p, v)]

        if matching_paths:
            return matching_paths[0]

        raise Exception("couldnt find matching endpoint")


def get_mock_http_component(map_of_responses: Dict[str, Tuple[Any, int]]):
    def wrapper(client):
        return DefaultHttpComponent(
            client, requests_dependency=MockRequests(map_of_responses)
        )

    return wrapper
