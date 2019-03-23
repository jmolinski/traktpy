# flake8: noqa: F403, F405

import time

import pytest
from tests.client import MockRequests
from tests.test_data.oauth import OAUTH_GET_TOKEN
from trakt import Trakt, TraktCredentials
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


TOKEN_REFRESH_HTTP = lambda client: DefaultHttpComponent(
    client,
    requests_dependency=MockRequests(
        {"countries/shows": [[], 200], "oauth/token": [OAUTH_GET_TOKEN, 200]}
    ),
)


def test_refresh_token_off():
    credentials = TraktCredentials("access", "refresh", "scope", 100)

    client = Trakt("", "", http_component=TOKEN_REFRESH_HTTP, user=credentials)
    client.get_countries(type="shows")

    assert client.user.refresh_token == "refresh"
    assert client.user.access_token == "access"


def test_refresh_token_on():
    client = Trakt("", "", http_component=TOKEN_REFRESH_HTTP, auto_refresh_token=True)

    # token is not going to expire soon (should not refresh)
    expire_at = int(time.time()) + 2 * 30 * 24 * 60 * 60  # 60 days
    client.set_user(TraktCredentials("access", "refresh", "scope", expire_at))
    client.get_countries(type="shows")

    assert client.user.refresh_token == "refresh"
    assert client.user.access_token == "access"

    # token is going to expire soon
    expire_at = int(time.time()) + 15 * 24 * 60 * 60  # 15 days
    client.set_user(TraktCredentials("access", "refresh", "scope", expire_at))
    client.get_countries(type="shows")

    assert client.user.refresh_token == OAUTH_GET_TOKEN["refresh_token"]
    assert client.user.access_token == OAUTH_GET_TOKEN["access_token"]
