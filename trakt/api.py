from trakt.config import DefaultConfig
from trakt.core.abstract import AbstractApi
from trakt.core.components import DefaultHttpComponent, DefaultOauthComponent
from trakt.core.executors import Executor
from trakt.core.paths import PATHS


class TraktApi(AbstractApi):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        http_component=None,
        oauth_component=None,
        **config: str
    ) -> None:
        self.authenticated = False
        self.client_id = client_id
        self.client_secret = client_secret

        self.config = DefaultConfig(
            client_id=client_id, client_secret=client_secret, **config
        )

        self.http = (http_component or DefaultHttpComponent)(self)
        self.oauth = (oauth_component or DefaultOauthComponent)(self)

    def noop(self) -> None:
        pass

    def __getattr__(self, item):
        e = Executor(self, item)
        e.install(PATHS)

        return e

    def request(self, params, *args, **kwargs):
        if isinstance(params, str):
            params = params.split(".")

        e = Executor(self, params)
        e.install(PATHS)

        return e.run(*args, **kwargs)
