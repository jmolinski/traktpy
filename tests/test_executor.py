# flake8: noqa: F403, F405

import pytest
from trakt import Trakt
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import ClientError


class MockHttpComponent(DefaultHttpComponent):
    def request(self, *args, **kwargs):
        return self.response


def test_executor():
    http = MockHttpComponent
    http.response = [{"name": "Australia", "code": "au"}]

    client = Trakt("", "", inject={"http_component": http})

    assert client.request("countries", type="shows") == http.response
    assert client.countries(type="shows") == http.response
    assert client.get_countries(type="shows") == http.response

    with pytest.raises(ClientError):
        client.count(type="shows")

    with pytest.raises(ClientError):
        client.countries()
