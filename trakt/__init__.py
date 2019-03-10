import logging
from logging import NullHandler
from typing import Any, Optional

from trakt.api import TraktApi  # NOQA
from trakt.version import __version__  # NOQA


class Trakt:
    _instance: Optional[TraktApi] = None

    def __getattr__(self, name: str) -> Any:
        if not self._instance:
            self._instance = TraktApi()

        return getattr(self._instance, name)


__all__ = (
    'Trakt',
)


logging.getLogger(__name__).addHandler(NullHandler())
