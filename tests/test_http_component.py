# flake8: noqa: F403, F405

import pytest
from tests.utils import MockRequests, mk_mock_client
from trakt import Trakt
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import BadRequest
from trakt.core.executors import Executor
from trakt.core.paths.path import Path


def test_get_url():
    client = Trakt("", "")

    url = client.http.get_url("a/b/c", {"d": "e"})

    assert url == "https://api.trakt.tv/a/b/c?d=e"


def test_bad_request_exception():
    client = Trakt("", "")

    http = DefaultHttpComponent(
        client, requests_dependency=MockRequests({".*": [{}, 400]})
    )

    with pytest.raises(BadRequest):
        http.request("...")


def test_extra_info_return():
    client = Trakt("", "")

    resp_headers = {
        "X-Pagination-Item-Count": 4,
        "X-Pagination-Limit": 1,
        "X-Pagination-Page": 2,
        "X-Pagination-Page-Count": 3,
    }
    http = DefaultHttpComponent(
        client,
        requests_dependency=MockRequests({".*": [{"a": "v"}, 200, resp_headers]}),
    )

    res, code, pagination = http.request(
        "abc", return_code=True, return_pagination=True
    )

    assert res == {"a": "v"}
    assert code == 200
    assert pagination["limit"] == 1
    assert pagination["page_count"] == 3


def test_add_quargs():
    client = mk_mock_client({".*": [[], 200]})
    path = Path("a", [None], qargs=["arg"])

    executor = Executor(client)

    _ = executor.run(path=path, arg="abc")

    req = client.http._requests.req_map["a"][0]

    url: str = req["path"]

    print(url)

    assert url.endswith(r"/a?arg=abc")
