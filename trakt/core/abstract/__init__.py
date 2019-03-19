from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from trakt.core.config import Config, TraktCredentials

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.components import DefaultHttpComponent, DefaultOauthComponent


class AbstractApi:
    client_id: str
    client_secret: str
    config: Config
    http: DefaultHttpComponent
    oauth: DefaultOauthComponent
    user: Optional[TraktCredentials]


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
