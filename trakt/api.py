from typing import Any

from trakt.config import Config, DefaultConfig
from trakt.core.abstract.abstract_api import AbstractApi
from trakt.core.components import HttpComponent, OathComponent


class TraktApi(AbstractApi):
    authenticated: bool
    client_id: str
    client_secret: str
    config: Config

    def __init__(self, client_id: str, client_secret: str, **config: str) -> None:
        self.authenticated = False
        self.client_id = client_id
        self.client_secret = client_secret

        self.config = DefaultConfig(
            client_id=client_id, client_secret=client_secret, **config
        )

        self.http = HttpComponent(self)
        self.oath = OathComponent(self)

    def noop(self) -> None:
        pass
