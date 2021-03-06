import json

import pytest
from tests.test_data.oauth import OAUTH_GET_TOKEN, OAUTH_VERIFICATION_CODE
from tests.utils import MockResponse, get_last_req, mk_mock_client
from trakt import Trakt, TraktCredentials
from trakt.core.components.oauth import CodeResponse
from trakt.core.exceptions import NotAuthenticated, TraktTimeoutError


def test_redirect_url():
    client = Trakt("123", "")

    url = client.oauth.get_redirect_url()

    exp_base = "https://api.trakt.tv/oauth/authorize"
    exp_args = "?response_type=code&client_id=123&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob"
    assert url == exp_base + exp_args


def test_get_token():
    client = mk_mock_client({".*": [OAUTH_GET_TOKEN, 200]})
    trakt_credentials = client.oauth.get_token(code="code", redirect_uri="uri")

    assert trakt_credentials.access_token == OAUTH_GET_TOKEN["access_token"]
    assert client.user
    assert client.user.access_token == OAUTH_GET_TOKEN["access_token"]


def test_revoke_token():
    client = mk_mock_client({".*": [{}, 200]}, user=None)
    user = TraktCredentials("access", "refresh", "scope", 100)

    assert client.user is None

    with pytest.raises(NotAuthenticated):
        client.oauth.revoke_token()

    client.set_user(user)
    assert client.user

    client.oauth.revoke_token()
    assert client.user is None


def test_get_verification_code():
    client = mk_mock_client({".*": [OAUTH_VERIFICATION_CODE, 200]}, client_id="123")

    code = client.oauth.get_verification_code()
    assert code.device_code == OAUTH_VERIFICATION_CODE["device_code"]
    assert json.loads(get_last_req(client.http)["data"])["client_id"] == "123"


def test_wait_for_response_success():
    def pool_endpoint_responses():
        yield MockResponse({}, 412)
        yield MockResponse([], 412)
        yield MockResponse(OAUTH_GET_TOKEN, 200)

    client = mk_mock_client(
        {
            ".*device/code.*": [OAUTH_VERIFICATION_CODE, 200],
            ".*device/token.*": pool_endpoint_responses(),
        },
        user=None,
    )
    client.oauth.sleep = lambda t: None

    assert client.user is None

    code = client.oauth.get_verification_code()
    client.oauth.wait_for_verification(code=code)

    assert client.user
    assert client.user.access_token == OAUTH_GET_TOKEN["access_token"]

    requests_log = client.http._requests.req_map["oauth/device/token"]
    assert len(requests_log) == 3


def test_wait_for_response_timeout():
    client = mk_mock_client({"device/token": [{}, 412]})
    client.oauth.sleep = lambda t: None

    code = CodeResponse(**OAUTH_VERIFICATION_CODE)

    with pytest.raises(TraktTimeoutError):
        client.oauth.wait_for_verification(code=code)
