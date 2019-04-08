from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from trakt.api import TraktApi


class AbstractBaseModel:
    _client: TraktApi

    @classmethod
    def set_client(cls, client: TraktApi) -> None:
        cls._client = client

    @property
    def client(self) -> TraktApi:
        return self._client

    def to_dict(self):
        return asdict(self)
