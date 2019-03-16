# flake8: noqa: F403, F405

from trakt import Trakt
from trakt.core.paths.path import Path
from trakt.core.components.http_component import DefaultHttpComponent


def test_oauth():
    client = Trakt("", "")

    url = client.http.get_url("a/b/c", {"d": "e"})

    assert url == "https://api.trakt.tv/a/b/c?d=e"


def test_redirect_url():
    client = Trakt("123", "")

    url = client.oauth.get_redirect_url()
    print(url)

    exp_base = "https://api.trakt.tv/oauth/authorize"
    exp_args = "?response_type=code&client_id=123&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob"
    assert url == exp_base + exp_args
