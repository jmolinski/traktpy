from __future__ import annotations

import time
from typing import NamedTuple

from trakt.core.abstract import AbstractComponent
from trakt.core.decorators import auth_required
from trakt.core.exceptions import ClientError


class TokenResponse(NamedTuple):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    scope: str
    created_at: int


class CodeResponse(NamedTuple):
    device_code: str
    user_code: str
    verification_url: str
    expires_in: int
    interval: int


class DefaultOauthComponent(AbstractComponent):
    name = "oauth"
    token = ""

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

    def get_token(self, *, code: str, redirect_uri: str = "") -> TokenResponse:
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

        token = TokenResponse(**ret)

        self.client.authenticated = True
        self.client.access_token = token.access_token
        self.token = token.access_token

        return token

    @auth_required
    def refresh_token(
        self, *, refresh_token: str, redirect_uri: str = ""
    ) -> TokenResponse:
        if not redirect_uri:
            redirect_uri = self.client.config["oauth"]["default_redirect_uri"]

        data = {
            "refresh_token": refresh_token,
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "refresh_token",
        }

        ret = self.client.http.request("oauth/token", method="POST", data=data)

        token = TokenResponse(**ret)

        self.client.authenticated = True
        self.client.access_token = token.access_token
        self.token = token.access_token

        return token

    @auth_required
    def revoke_token(self) -> None:
        data = {
            "token": self.token,
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
        }

        self.client.http.request("oauth/revoke", method="POST", data=data, headers={})

        self.client.authenticated = False
        self.client.access_token = ""
        self.token = ""

    def get_verification_code(self) -> CodeResponse:
        data = {"client_id": self.client.client_id}

        ret = self.client.http.request(
            "oauth/device/code", method="POST", data=data, headers={}
        )

        return CodeResponse(**ret)

    def wait_for_verification(self, *, code: CodeResponse) -> TokenResponse:
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
                raise ClientError("Code expired; start the verification process again")

            time.sleep(code.interval + 0.3)

        token = TokenResponse(**ret)

        self.client.authenticated = True
        self.client.access_token = token.access_token
        self.token = token.access_token

        return token
