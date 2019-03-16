import json

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
    def __init__(self, json_response, code=200):
        self.response = MockResponse(json_response, code)

    def request(self, *args, **kwargs):
        return self.response


def get_mock_http_component(response=None, code=200):
    response = response or {}

    def wrapper(client):
        return DefaultHttpComponent(
            client, requests_dependency=MockRequests(json_response=response, code=code)
        )

    return wrapper
