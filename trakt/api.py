from typing import Any

from trakt.config import Config, DefaultConfig
from trakt.core.abstract_api import AbstractApi


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

    def login(self) -> None:
        pass

    def request(self, path: str, *args: Any, **kwargs: Any) -> Any:
        pass

    def noop(self) -> None:
        pass
