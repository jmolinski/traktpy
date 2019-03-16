import logging
from logging import NullHandler
from typing import Any, Dict, Optional

from trakt.api import TraktApi
from trakt.core.abstract import AbstractBaseModel
from trakt.version import __version__  # NOQA


class Trakt:
    _instance: Optional[TraktApi] = None
    _config: Dict[str, Any]
    _injected: Dict[str, Any]

    def __init__(
        self, client_id: str, client_secret: str, *, inject: Dict[str, Any] = None
    ) -> None:
        self._config = {"client_id": client_id, "client_secret": client_secret}
        self._injected = inject or {}

    def __getattr__(self, name: str) -> Any:
        if not self._instance:
            self._instance = TraktApi(**self._config, **self._injected)
            AbstractBaseModel.set_client(self._instance)

        return getattr(self._instance, name)


__all__ = ("Trakt",)


logging.getLogger(__name__).addHandler(NullHandler())
