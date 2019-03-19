import logging
from logging import NullHandler

from trakt.api import TraktApi, TraktCredentials
from trakt.version import __version__  # NOQA

Trakt = TraktApi

__all__ = ("Trakt", "TraktCredentials")


logging.getLogger(__name__).addHandler(NullHandler())
