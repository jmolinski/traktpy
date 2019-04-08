from __future__ import annotations

import time
from typing import TYPE_CHECKING, NamedTuple, cast

from trakt.core.config import TraktCredentials
from trakt.core.decorators import auth_required
from trakt.core.exceptions import TraktTimeoutError

if TYPE_CHECKING:  # pragma: no cover
    from trakt.api import TraktApi


class CodeResponse(NamedTuple):
    device_code: str
    user_code: str
    verification_url: str
    expires_in: int
    interval: int


class DefaultOauthComponent:
    name = "oauth"
    client: TraktApi

    def __init__(self, client: TraktApi) -> None:
        self.client = client

    def get_redirect_url(self, *, redirect_uri: str = "", state: str = "") -> str:
        if not redirect_uri:
            redirect_uri = self.client.config["oauth"]["default_redirect_uri"]

        quargs = {
            "response_type": "code",
            "client_id": self.client.client_id,
            "redirect_uri": redirect_uri,
        }

        if state:
            quargs["state"] = state

        return self.client.http.get_url("oauth/authorize", query_args=quargs)

    def get_token(self, *, code: str, redirect_uri: str = "") -> TraktCredentials:
        if not redirect_uri:
            redirect_uri = self.client.config["oauth"]["default_redirect_uri"]

        data = {
            "code": code,
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        ret = self.client.http.request("oauth/token", method="POST", data=data)

        self.client.user = TraktCredentials(
            access_token=ret["access_token"],
            refresh_token=ret["refresh_token"],
            scope=ret["scope"],
            expires_at=(int(ret["created_at"]) + int(ret["expires_in"])),
        )

        return self.client.user

    @auth_required
    def refresh_token(self, *, redirect_uri: str = "") -> TraktCredentials:
        if not redirect_uri:
            redirect_uri = self.client.config["oauth"]["default_redirect_uri"]

        data = {
            "refresh_token": cast(TraktCredentials, self.client.user).access_token,
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "refresh_token",
        }

        ret = self.client.http.request("oauth/token", method="POST", data=data)

        self.client.user = TraktCredentials(
            access_token=ret["access_token"],
            refresh_token=ret["refresh_token"],
            scope=ret["scope"],
            expires_at=(int(ret["created_at"]) + int(ret["expires_in"])),
        )

        return self.client.user

    @auth_required
    def revoke_token(self) -> None:
        data = {
            "token": cast(TraktCredentials, self.client.user).access_token,
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
        }

        self.client.http.request("oauth/revoke", method="POST", data=data, headers={})

        self.client.user = None

    def get_verification_code(self) -> CodeResponse:
        data = {"client_id": self.client.client_id}

        ret = self.client.http.request(
            "oauth/device/code", method="POST", data=data, headers={}
        )

        return CodeResponse(**ret)

    def wait_for_verification(self, *, code: CodeResponse) -> TraktCredentials:
        data = {
            "code": code.device_code,
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
        }

        elapsed_time: float = 0
        while True:
            ret, status_code = self.client.http.request(
                "oauth/device/token",
                method="POST",
                data=data,
                return_code=True,
                headers={},
                no_raise=True,
            )
            if status_code == 200:
                break

            elapsed_time += code.interval + 0.3
            if elapsed_time > code.expires_in:
                raise TraktTimeoutError(
                    message="Code expired; start the verification process again"
                )

            self.sleep(code.interval + 0.3)

        self.client.user = TraktCredentials(
            access_token=ret["access_token"],
            refresh_token=ret["refresh_token"],
            scope=ret["scope"],
            expires_at=(int(ret["created_at"]) + int(ret["expires_in"])),
        )

        return self.client.user

    def sleep(self, t: float):  # pragma: no cover
        return time.sleep(t)
