import logging
from logging import NullHandler

from trakt.api import TraktApi
from trakt.version import __version__  # NOQA

Trakt = TraktApi

__all__ = ("Trakt",)


logging.getLogger(__name__).addHandler(NullHandler())
