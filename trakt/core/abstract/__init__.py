from __future__ import annotations

from typing import TYPE_CHECKING

from trakt.core.config import Config

if TYPE_CHECKING:
    from trakt.core.components import DefaultHttpComponent, DefaultOauthComponent


class AbstractApi:
    authenticated: bool
    client_id: str
    client_secret: str
    config: Config
    http: DefaultHttpComponent
    oauth: DefaultOauthComponent
    access_token: str


class AbstractComponent:
    name: str = "base_component"
    client: AbstractApi

    def __init__(self, client: AbstractApi) -> None:
        self.client = client


class AbstractBaseModel:
    _client = AbstractApi()

    @classmethod
    def set_client(cls, client: AbstractApi) -> None:
        cls._client = client

    @property
    def client(self) -> AbstractApi:
        return self._client
