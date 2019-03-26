from tests.client import get_mock_http_component
from tests.test_data.oauth import OAUTH_GET_TOKEN
from trakt import Trakt


def test_redirect_url():
    client = Trakt("123", "")

    url = client.oauth.get_redirect_url()

    exp_base = "https://api.trakt.tv/oauth/authorize"
    exp_args = "?response_type=code&client_id=123&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob"
    assert url == exp_base + exp_args


def test_get_token():
    client = Trakt(
        "", "", http_component=get_mock_http_component({".*": [OAUTH_GET_TOKEN, 200]})
    )

    trakt_credentials = client.oauth.get_token(code="code", redirect_uri="uri")

    assert trakt_credentials.access_token == OAUTH_GET_TOKEN["access_token"]
    assert client.user
    assert client.user.access_token == OAUTH_GET_TOKEN["access_token"]
