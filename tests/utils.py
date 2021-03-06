import json
import re
import types
from collections import defaultdict
from copy import deepcopy
from math import ceil
from typing import Any, Dict, Generator, Iterable, List, Optional

from trakt import Trakt, TraktCredentials
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
        self.req_stack = []
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
        def response_generator():
            while True:
                yield MockResponse(json_response, code, headers)

        return response_generator()

    def request(self, method, path, params, *args, **kwargs):
        p = path.split(".tv/" if ".tv" in path else ".com/")[1]

        if params:
            path += "?" + "&".join([f"{k}={v}" for k, v in params.items()])

        # log request
        req = {
            **kwargs,
            "method": method,
            "path": path,
            "resource": p,
            "params": params,
        }
        self.req_map[p].append(req)
        self.req_stack.append(req)

        endpoint_identifier = self.find_path(path)
        response = next(self.m[endpoint_identifier])

        if endpoint_identifier[2:-2] in self.paginated_endpoints:
            return self.return_page(response, params=params, **kwargs)

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


USER = TraktCredentials("", "", "", 10e14)


def mk_mock_client(
    endpoints, client_id="", client_secret="", user=False, paginated=None, **config
):
    return Trakt(
        client_id,
        client_secret,
        http_component=get_mock_http_component(endpoints, paginated=paginated),
        user=USER if user is False else None,
        **config,
    )


def get_last_req(http):
    if http._requests.req_stack:
        return http._requests.req_stack[-1]
