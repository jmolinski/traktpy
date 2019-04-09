# flake8: noqa: F403, F405

import time
from dataclasses import asdict

import pytest
from tests.test_data.oauth import OAUTH_GET_TOKEN
from tests.utils import MockRequests, get_last_req, mk_mock_client
from trakt import Trakt, TraktCredentials
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import ArgumentError, ClientError
from trakt.core.executors import Executor, PaginationIterator
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
    client = mk_mock_client(
        {"pag_off": [data, 200], "pag_on": [data, 200]}, paginated=["pag_on"]
    )
    executor = Executor(client)

    p_nopag = Path("pag_off", [int])
    p_pag = Path("pag_on", [int], pagination=True)

    res_nopag = executor.run(path=p_nopag)
    res_pag = executor.run(path=p_pag, page=2, per_page=3)

    assert isinstance(res_nopag, list)
    assert res_nopag == data

    assert isinstance(res_pag, PaginationIterator)
    assert list(executor.run(path=p_pag, page=2, per_page=4)) == [5, 6, 7, 8, 9, 10]


def test_prefetch_off():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    client = mk_mock_client({"pag_on": [data, 200]}, paginated=["pag_on"])
    executor = Executor(client)
    p_pag = Path("pag_on", [int], pagination=True)

    assert get_last_req(client.http) is None
    req = executor.run(path=p_pag, page=2, per_page=3)
    assert get_last_req(client.http) is None
    list(req)
    assert get_last_req(client.http) is not None


def test_prefetch_on():
    data = list(range(10 ** 4))
    client = mk_mock_client({"pag_on": [data, 200]}, paginated=["pag_on"])
    executor = Executor(client)
    p_pag = Path("pag_on", [int], pagination=True)

    # prefetch
    assert get_last_req(client.http) is None
    req = executor.run(path=p_pag, page=2, per_page=3)
    assert get_last_req(client.http) is None
    req.prefetch_all()
    assert get_last_req(client.http) is not None

    # reset history
    client.http._requests.req_stack = []
    assert get_last_req(client.http) is None

    # execute prefetched -> assert no new requests
    list(req)
    assert get_last_req(client.http) is None


def test_take():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    client = mk_mock_client({"pag_on": [data, 200]}, paginated=["pag_on"])
    executor = Executor(client)
    p_pag = Path("pag_on", [int], pagination=True)

    it = executor.run(path=p_pag, per_page=2)
    assert it.has_next()
    assert isinstance(next(it), int)
    assert next(it) == 2
    assert it.has_next()

    assert it.take(3) == [3, 4, 5]
    assert it.has_next()

    with pytest.raises(ArgumentError):
        it.take(-5)

    assert it.take(0) == []
    assert it.take() == [6, 7]  # per_page setting
    assert it.has_next()

    assert it.take_all() == [8, 9, 10]
    assert not it.has_next()

    with pytest.raises(StopIteration):
        next(it)

    assert it.take(2) == it.take_all() == []


def test_chaining():
    data = list(range(300))
    client = mk_mock_client({"pag_on": [data, 200]}, paginated=["pag_on"])
    executor = Executor(client)
    p_pag = Path("pag_on", [int], pagination=True)

    assert executor.run(path=p_pag, per_page=2).take_all() == data
    assert executor.run(path=p_pag, per_page=2).prefetch_all().take_all() == data
