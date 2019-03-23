from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Type, Union

from trakt.core.abstract import AbstractApi, AbstractBaseModel
from trakt.core.components import DefaultHttpComponent, DefaultOauthComponent
from trakt.core.config import DefaultConfig, TraktCredentials
from trakt.core.executors import Executor
from trakt.core.paths import CalendarsInterface, CountriesInterface

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.paths.suite_interface import SuiteInterface


class TraktApi(AbstractApi):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        http_component: Optional[Type[DefaultHttpComponent]] = None,
        oauth_component: Optional[Type[DefaultOauthComponent]] = None,
        countries_interface: Optional[Type[CountriesInterface]] = None,
        calendars_interface: Optional[Type[CalendarsInterface]] = None,
        user: Optional[TraktCredentials] = None,
        auto_refresh_token: bool = False,
        **config: str
    ) -> None:
        AbstractBaseModel.set_client(self)

        self.client_id = client_id
        self.client_secret = client_secret

        self.config = DefaultConfig(
            client_id=client_id,
            client_secret=client_secret,
            auto_refresh_token=auto_refresh_token,
            **config
        )

        self.user = user

        self.http = (http_component or DefaultHttpComponent)(self)
        self.oauth = (oauth_component or DefaultOauthComponent)(self)
        self.countries = (countries_interface or CountriesInterface)(self, Executor)
        self.calendars = (calendars_interface or CalendarsInterface)(self, Executor)

    def request(self, params: Union[str, List[str]], **kwargs: Any) -> Any:
        if isinstance(params, str):
            params = params.split(".")

        e = Executor(self, params)
        e.install(self._get_executor_paths())

        return e.run(**kwargs)

    def set_user(self, user: TraktCredentials) -> None:
        self.user = user

    def __getattr__(self, item: str) -> Executor:
        e = Executor(self, item)
        e.install(self._get_executor_paths())

        return e

    def _get_executor_paths(self) -> List[SuiteInterface]:
        return [self.countries, self.calendars]
