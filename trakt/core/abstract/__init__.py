from __future__ import annotations

from typing import Any, Dict, Type, TypeVar, cast

import jsons
from trakt.config import Config


class AbstractApi:
    authenticated: bool
    client_id: str
    client_secret: str
    config: Config
    http: "AbstractComponent"


class AbstractComponent:
    name: str = "base_component"
    client: AbstractApi

    def __init__(self, client: AbstractApi) -> None:
        self.client = client


class _AbstractFromJson:
    pass


T = TypeVar("T", bound=_AbstractFromJson)


class AbstractBaseModel(_AbstractFromJson):
    _client = AbstractApi()

    @classmethod
    def from_json(cls: Type[T], data: Dict[str, Any]) -> T:
        obj = jsons.load(data, cls)
        return cast(T, obj)

    @classmethod
    def set_client(cls, client: AbstractApi) -> None:
        cls._client = client

    @property
    def client(self) -> AbstractApi:
        return self._client
