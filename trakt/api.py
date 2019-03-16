from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Type, Union

from trakt.config import DefaultConfig
from trakt.core.abstract import AbstractApi
from trakt.core.components import DefaultHttpComponent, DefaultOauthComponent
from trakt.core.executors import Executor
from trakt.core.paths import CountriesInterface

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.paths.suite_interface import SuiteInterface


class TraktApi(AbstractApi):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        http_component: Optional[Type[DefaultHttpComponent]] = None,
        oauth_component: Optional[Type[DefaultOauthComponent]] = None,
        countries_interface: Any = None,
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

        self.countries = (countries_interface or CountriesInterface)(self, Executor)

    def noop(self) -> None:
        pass

    def __getattr__(self, item: str) -> Executor:
        e = Executor(self, item)
        e.install(self.get_executor_paths())

        return e

    def request(self, params: Union[str, List[str]], **kwargs: Any) -> Any:
        if isinstance(params, str):
            params = params.split(".")

        e = Executor(self, params)
        e.install(self.get_executor_paths())

        return e.run(**kwargs)

    def get_executor_paths(self) -> List[SuiteInterface]:
        return [self.countries]
