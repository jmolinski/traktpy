from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Type, Union

from trakt.core.abstract import AbstractApi, AbstractBaseModel
from trakt.core.components import DefaultHttpComponent, DefaultOauthComponent
from trakt.core.config import DefaultConfig, TraktCredentials
from trakt.core.executors import Executor
from trakt.core.paths import (
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


class TraktApi(AbstractApi):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        http_component: Optional[Type[DefaultHttpComponent]] = None,
        oauth_component: Optional[Type[DefaultOauthComponent]] = None,
        countries_interface: Optional[Type[CountriesI]] = None,
        calendars_interface: Optional[Type[CalendarsI]] = None,
        shows_interface: Optional[Type[ShowsI]] = None,
        genres_interface: Optional[Type[GenresI]] = None,
        certifications_interface: Optional[Type[CertificationsI]] = None,
        languages_interface: Optional[Type[LanguagesI]] = None,
        lists_interface: Optional[Type[ListsI]] = None,
        movies_interface: Optional[Type[MoviesI]] = None,
        checkin_interface: Optional[Type[CheckinI]] = None,
        people_interface: Optional[Type[PeopleI]] = None,
        networks_interface: Optional[Type[NetworksI]] = None,
        comments_interface: Optional[Type[CommentsI]] = None,
        search_interface: Optional[Type[SearchI]] = None,
        recommendations_interface: Optional[Type[RecommendationsI]] = None,
        scrobble_interface: Optional[Type[ScrobbleI]] = None,
        seasons_interface: Optional[Type[SeasonsI]] = None,
        episodes_interface: Optional[Type[EpisodesI]] = None,
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
        self.countries = (countries_interface or CountriesI)(self, Executor)
        self.calendars = (calendars_interface or CalendarsI)(self, Executor)
        self.shows = (shows_interface or ShowsI)(self, Executor)
        self.genres = (genres_interface or GenresI)(self, Executor)
        self.certifications = (certifications_interface or CertificationsI)(
            self, Executor
        )
        self.languages = (languages_interface or LanguagesI)(self, Executor)
        self.lists = (lists_interface or ListsI)(self, Executor)
        self.movies = (movies_interface or MoviesI)(self, Executor)
        self.checkin = (checkin_interface or CheckinI)(self, Executor)
        self.people = (people_interface or PeopleI)(self, Executor)
        self.networks = (networks_interface or NetworksI)(self, Executor)
        self.comments = (comments_interface or CommentsI)(self, Executor)
        self.search = (search_interface or SearchI)(self, Executor)
        self.recommendations = (recommendations_interface or RecommendationsI)(
            self, Executor
        )
        self.scrobble = (scrobble_interface or ScrobbleI)(self, Executor)
        self.seasons = (seasons_interface or SeasonsI)(self, Executor)
        self.episodes = (episodes_interface or EpisodesI)(self, Executor)

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
        return [
            self.calendars,
            self.certifications,
            self.comments,
            self.countries,
            self.genres,
            self.shows,
            self.languages,
            self.lists,
            self.movies,
            self.people,
            self.networks,
            self.recommendations,
            self.scrobble,
            self.search,
        ]
