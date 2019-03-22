# flake8: noqa: F403, F405

import pytest
from tests.client import MockRequests
from trakt import Trakt
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import BadRequest


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
