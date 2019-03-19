# flake8: noqa: F403, F405

import pytest
from tests.client import MockRequests
from trakt import Trakt
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import ClientError


def test_executor():
    response = [{"name": "Australia", "code": "au"}]
    http = lambda client: DefaultHttpComponent(
        client, requests_dependency=MockRequests({"*": [response, 200]})
    )

    client = Trakt("", "", http_component=http)

    assert client.request("countries", type="shows") == response
    assert client.request("get_countries", type="shows") == response
    assert client.request("countries.get_countries", type="shows") == response
    assert client.get_countries(type="shows") == response

    with pytest.raises(ClientError):
        client.count(type="shows")


def test_refresh_token():
    pass
