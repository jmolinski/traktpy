from __future__ import annotations

from typing import Any

from trakt.config import Config


class AbstractApi:
    authenticated: bool
    client_id: str
    client_secret: str
    config: Config
    http: AbstractComponent
    oauth: AbstractComponent


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


class AbstractSuiteInterface:
    def __init__(self, client: AbstractApi) -> None:
        raise NotImplementedError

    def find_match(self, name: str) -> None:
        raise NotImplementedError

    def run(self, command: str, **kwargs: Any):
        raise NotImplementedError
