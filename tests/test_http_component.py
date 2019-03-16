# flake8: noqa: F403, F405

import pytest
from trakt import Trakt
from trakt.core.components import DefaultHttpComponent
from trakt.core.exceptions import BadRequest

from tests.client import MockRequests


def test_bad_request_exception():
    client = Trakt("", "")

    http = DefaultHttpComponent(
        client, requests_dependency=MockRequests(json_response={}, code=400)
    )

    with pytest.raises(BadRequest):
        http.request("...")
