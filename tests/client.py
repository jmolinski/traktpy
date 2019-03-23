import json
import re
from collections import defaultdict
from math import ceil
from typing import Any, Dict, List, Optional, Tuple

from trakt.core.components.http_component import DefaultHttpComponent

try:
    with open(".secrets") as f:
        SECRETS = json.loads(f.read())
except:  # NOQA
    SECRETS = {"client_secret": "", "client_id": ""}


class MockResponse:
    def __init__(self, json_response, code, headers):
        self.status_code = code
        self.json_response = json_response
        self.original_json = json_response
        self.headers = headers

    def json(self):
        return self.json_response

    def set_headers(self, headers):
        self.headers.update(headers)


class MockRequests:
    def __init__(self, map_of_responses, paginated=None):
        self.m = {}
        self.req_map = defaultdict(list)
        self.paginated_endpoints = paginated or set()

        for path, (json_response, code, *rest) in map_of_responses.items():
            headers = {} if not rest else rest[0]
            self.m[".*" + path + ".*"] = MockResponse(json_response, code, headers)

    def request(self, method, path, *args, **kwargs):
        p = path.split(".tv/" if ".tv" in path else ".com/")[1]

        # log request
        self.req_map[p].append(
            {**kwargs, "method": method, "path": path, "resource": p}
        )

        endpoint_identifier = self.find_path(path)

        if endpoint_identifier[2:-2] in self.paginated_endpoints:
            return self.return_page(endpoint_identifier, **kwargs)

        return self.m[endpoint_identifier]

    def find_path(self, v):
        paths = set(self.m.keys())
        matching_paths = [p for p in paths if re.match(p, v)]

        if matching_paths:
            return matching_paths[0]

        raise Exception("couldnt find matching endpoint")

    def return_page(self, endpoint_identifier, params=None, **kwargs):
        response = self.m[endpoint_identifier]

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
    map_of_responses: Dict[str, Tuple[Any, int]], paginated: Optional[List[str]] = None
):
    paginated = paginated or []

    def wrapper(client):
        return DefaultHttpComponent(
            client, requests_dependency=MockRequests(map_of_responses, paginated)
        )

    return wrapper
