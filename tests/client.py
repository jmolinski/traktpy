import json
import re
import types
from collections import defaultdict
from copy import deepcopy
from math import ceil
from typing import Any, Dict, Generator, Iterable, List, Optional

from trakt.core.components.http_component import DefaultHttpComponent

try:
    with open(".secrets") as f:
        SECRETS = json.loads(f.read())
except:  # NOQA
    SECRETS = {"client_secret": "", "client_id": ""}


class MockResponse:
    def __init__(self, json_response=None, code=200, headers=None):
        self.status_code = code
        self.json_response = json_response or {}
        self.original_json = json_response or {}
        self.headers = headers or {}

    def json(self):
        return self.json_response

    def set_headers(self, headers):
        self.headers.update(headers)


class MockRequests:
    def __init__(self, map_of_responses, paginated=None):
        self.m: Dict[str, Generator[MockResponse, None, None]] = {}
        self.req_map = defaultdict(list)
        self.paginated_endpoints = paginated or set()

        for path, v in map_of_responses.items():
            regexified_path = ".*" + path + ".*"

            if isinstance(v, list):
                (json_response, code, *rest) = v
                headers = {} if not rest else rest[0]

                self.m[regexified_path] = self.make_infinite_response_generator(
                    json_response, code, headers
                )

            elif isinstance(v, types.GeneratorType):
                self.m[regexified_path] = v
            else:
                raise Exception(
                    "invalid response arg; must be [json, code, ?headers] or a generator of such"
                )

    def make_infinite_response_generator(self, json_response, code, headers):
        jr = deepcopy(json_response)
        c = deepcopy(code)
        h = deepcopy(headers)

        def response_generator():
            while True:
                yield MockResponse(jr, c, h)

        return response_generator()

    def request(self, method, path, *args, **kwargs):
        p = path.split(".tv/" if ".tv" in path else ".com/")[1]

        # log request
        self.req_map[p].append(
            {**kwargs, "method": method, "path": path, "resource": p}
        )

        endpoint_identifier = self.find_path(path)
        response = next(self.m[endpoint_identifier])

        if endpoint_identifier[2:-2] in self.paginated_endpoints:
            return self.return_page(response, **kwargs)

        return response

    def find_path(self, v):
        paths = set(self.m.keys())
        matching_paths = [p for p in paths if re.match(p, v)]

        if len(matching_paths) == 1:
            return matching_paths[0]

        raise Exception(f"found {len(matching_paths)} matching endpoints")

    def return_page(self, response, params=None, **kwargs):
        page = int(params["page"])
        limit = int(params["limit"])

        headers = {
            "X-Pagination-Item-Count": str(len(response.original_json)),
            "X-Pagination-Limit": str(limit),
            "X-Pagination-Page": str(page),
            "X-Pagination-Page-Count": str(ceil(len(response.original_json) / limit)),
        }

        offset = (page - 1) * limit
        response.json_response = response.original_json[offset : offset + limit]
        response.set_headers(headers)

        return response


def get_mock_http_component(
    map_of_responses: Dict[str, Iterable[Any]], paginated: Optional[List[str]] = None
):
    paginated = paginated or []

    def wrapper(client):
        return DefaultHttpComponent(
            client, requests_dependency=MockRequests(map_of_responses, paginated)
        )

    return wrapper
