import json

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
    def __init__(self, json_response, code):
        self.response = MockResponse(json_response, code)

    def request(self, *args, **kwargs):
        return self.response
