# flake8: noqa: F403, F405

import types

import pytest
from tests.client import MockRequests
from tests.test_data.countries import COUNTRIES
from tests.test_data.oauth import OAUTH_GET_TOKEN
from trakt import Trakt, TraktCredentials
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import ClientError
from trakt.core.executors import Executor
from trakt.core.paths import Path


def test_executor():
    response = [{"name": "Australia", "code": "au"}]
    http = lambda client: DefaultHttpComponent(
        client, requests_dependency=MockRequests({".*": [response, 200]})
    )

    client = Trakt("", "", http_component=http)

    assert client.request("countries", type="shows") == response
    assert client.request("get_countries", type="shows") == response
    assert client.request("countries.get_countries", type="shows") == response
    assert client.get_countries(type="shows") == response

    with pytest.raises(ClientError):
        client.count(type="shows")


def test_refresh_token():
    http = lambda client: DefaultHttpComponent(
        client,
        requests_dependency=MockRequests(
            {"countries/shows": [COUNTRIES, 200], "oauth/token": [OAUTH_GET_TOKEN, 200]}
        ),
    )

    credentials = TraktCredentials("access", "refresh", "scope", 100)

    ### refresh off

    client = Trakt("", "", http_component=http, user=credentials)
    client.get_countries(type="shows")

    assert client.user.refresh_token == "refresh"
    assert client.user.access_token == "access"

    ### refresh on

    client = Trakt(
        "", "", http_component=http, user=credentials, auto_refresh_token=True
    )
    client.get_countries(type="shows")

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
