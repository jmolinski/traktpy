# flake8: noqa: F403, F405

import pytest
from trakt import Trakt
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import BadRequest


class MockResponse:
    def __init__(self, json_response, code):
        self.status_code = code
        self.json_response = json_response

    def json(self):
        return self.json_response


class MockRequests:
    def __init__(self, json_response, code):
        self.response = MockResponse(json_response, code)

    def request(self, *args, **kwargs):
        return self.response


def test_bad_request_exception():
    client = Trakt("", "")

    http = DefaultHttpComponent(
        client, requests_dependency=MockRequests(json_response={}, code=400)
    )

    with pytest.raises(BadRequest):
        http.request("...")
