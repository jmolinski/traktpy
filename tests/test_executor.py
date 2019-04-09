# flake8: noqa: F403, F405

import time
import types
from dataclasses import asdict

import pytest
from tests.test_data.oauth import OAUTH_GET_TOKEN
from tests.utils import MockRequests, mk_mock_client
from trakt import Trakt, TraktCredentials
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import ClientError
from trakt.core.executors import Executor
from trakt.core.paths import Path


def test_executor():
    response = [{"name": "Australia", "code": "au"}]
    client = mk_mock_client({".*": [response, 200]})

    assert len(client.request("countries", type="shows")) == len(response)
    assert len(client.request("countries.get_countries", type="shows")) == len(response)

    countries = client.request("get_countries", type="shows")
    assert [asdict(s) for s in countries] == response

    with pytest.raises(ClientError):
        client.request("count", type="shows")


TOKEN_REFRESH_HTTP = lambda client: DefaultHttpComponent(
    client,
    requests_dependency=MockRequests(
        {"countries/shows": [[], 200], "oauth/token": [OAUTH_GET_TOKEN, 200]}
    ),
)


def test_refresh_token_off():
    credentials = TraktCredentials("access", "refresh", "scope", 100)

    client = Trakt("", "", http_component=TOKEN_REFRESH_HTTP, user=credentials)
    client.countries.get_countries(type="shows")

    assert client.user.refresh_token == "refresh"
    assert client.user.access_token == "access"


def test_refresh_token_on():
    client = Trakt("", "", http_component=TOKEN_REFRESH_HTTP, auto_refresh_token=True)

    # token is not going to expire soon (should not refresh)
    expire_at = int(time.time()) + 2 * 30 * 24 * 60 * 60  # 60 days
    client.set_user(TraktCredentials("access", "refresh", "scope", expire_at))
    client.countries.get_countries(type="shows")

    assert client.user.refresh_token == "refresh"
    assert client.user.access_token == "access"

    # token is going to expire soon
    expire_at = int(time.time()) + 15 * 24 * 60 * 60  # 15 days
    client.set_user(TraktCredentials("access", "refresh", "scope", expire_at))
    client.countries.get_countries(type="shows")

    assert client.user.refresh_token == OAUTH_GET_TOKEN["refresh_token"]
    assert client.user.access_token == OAUTH_GET_TOKEN["access_token"]


def test_pagination():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    http = lambda client: DefaultHttpComponent(
        client,
        requests_dependency=MockRequests(
            {"pag_off": [data, 200], "pag_on": [data, 200]}, paginated=["pag_on"]
        ),
    )

    client = Trakt("", "", http_component=http)
    executor = Executor(client)

    p_nopag = Path("pag_off", [int])
    p_pag = Path("pag_on", [int], pagination=True)

    res_nopag = executor.run(path=p_nopag)
    res_pag = executor.run(path=p_pag, page=2, per_page=3)

    assert isinstance(res_nopag, list)
    assert res_nopag == data

    assert isinstance(res_pag, types.GeneratorType)
    assert list(executor.run(path=p_pag, page=2, per_page=4)) == [5, 6, 7, 8, 9, 10]
