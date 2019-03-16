from __future__ import annotations

from typing import NamedTuple

from trakt.core.abstract import AbstractComponent


class TokenResponse(NamedTuple):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    scope: str
    created_at: int


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

        return token
