from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union

from trakt.core.components import (
    CacheManager,
    DefaultHttpComponent,
    DefaultOauthComponent,
)
from trakt.core.config import Config, DefaultConfig, TraktCredentials
from trakt.core.executors import Executor
from trakt.core.models import AbstractBaseModel
from trakt.core.paths import (
    DEFAULT_INTERFACES,
    CalendarsI,
    CertificationsI,
    CheckinI,
    CommentsI,
    CountriesI,
    EpisodesI,
    GenresI,
    LanguagesI,
    ListsI,
    MoviesI,
    NetworksI,
    PeopleI,
    RecommendationsI,
    ScrobbleI,
    SearchI,
    SeasonsI,
    ShowsI,
)

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.paths.suite_interface import SuiteInterface


CACHE_LEVELS = CacheManager.CACHE_LEVELS


class TraktApi:
    client_id: str
    client_secret: str
    config: Config
    http: DefaultHttpComponent
    oauth: DefaultOauthComponent
    cache: CacheManager
    user: Optional[TraktCredentials]

    countries: CountriesI
    calendars: CalendarsI
    shows: ShowsI
    genres: GenresI
    certifications: CertificationsI
    languages: LanguagesI
    lists: ListsI
    movies: MoviesI
    checkin: CheckinI
    people: PeopleI
    networks: NetworksI
    comments: CommentsI
    search: SearchI
    recommendations: RecommendationsI
    scrobble: ScrobbleI
    seasons: SeasonsI
    episodes: EpisodesI

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        http_component: Optional[Type[DefaultHttpComponent]] = None,
        oauth_component: Optional[Type[DefaultOauthComponent]] = None,
        cache_manager: Optional[Type[CacheManager]] = None,
        interfaces: Dict[str, Type[SuiteInterface]] = None,
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
        self.cache = (cache_manager or CacheManager)(self)

        interfaces = interfaces or {}
        for i_name, default in DEFAULT_INTERFACES.items():
            i_obj = interfaces.get(i_name, default)(self, Executor)
            setattr(self, i_name, i_obj)

    def request(self, params: Union[str, List[str]], **kwargs: Any) -> Any:
        if isinstance(params, str):
            params = params.split(".")

        e = Executor(self, params)
        e.install(self._get_executor_paths())

        return e.run(**kwargs)

    def set_user(self, user: TraktCredentials) -> None:
        self.user = user

    def _get_executor_paths(self) -> List[SuiteInterface]:
        return [
            self.calendars,
            self.certifications,
            self.comments,
            self.countries,
            self.genres,
            self.languages,
            self.lists,
            self.movies,
            self.people,
            self.networks,
            self.recommendations,
            self.scrobble,
            self.search,
            self.shows,
        ]
