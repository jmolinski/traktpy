from typing import Any, Iterable, List

from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    Certification,
    Country,
    Genre,
    Language,
    ListResponse,
    Network,
    TrendingShow,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import COMMON_FILTERS, SHOWS_FILTERS, PerArgValidator

TYPE_MOVIES_SHOWS = PerArgValidator("type", lambda t: t in {"shows", "movies"})


class CountriesI(SuiteInterface):
    name = "countries"

    paths = {
        "get_countries": Path(
            "countries/!type",
            [Country],
            aliases=["get_countries", ""],
            validators=[TYPE_MOVIES_SHOWS],
        )
    }

    def get_countries(self, *, type: str, **kwargs: Any) -> List[Country]:
        return self.run("get_countries", type=type, **kwargs)


class CertificationsI(SuiteInterface):
    name = "certifications"

    paths = {
        "get_certifications": Path(
            "certifications/!type",
            {"us": [Certification]},
            validators=[TYPE_MOVIES_SHOWS],
        )
    }

    def get_certifications(self, *, type: str, **kwargs: Any) -> List[Certification]:
        ret = self.run("get_certifications", type=type, **kwargs)
        return ret["us"]


class GenresI(SuiteInterface):
    name = "genres"

    paths = {
        "get_genres": Path("genres/!type", [Genre], validators=[TYPE_MOVIES_SHOWS])
    }

    def get_genres(self, *, type: str, **kwargs: Any) -> List[Genre]:
        return self.run("get_genres", type=type, **kwargs)


class LanguagesI(SuiteInterface):
    name = "languages"

    paths = {
        "get_languages": Path(
            "languages/!type", [Language], validators=[TYPE_MOVIES_SHOWS]
        )
    }

    def get_languages(self, *, type: str, **kwargs: Any) -> List[Language]:
        return self.run("get_languages", type=type, **kwargs)


class ShowsI(SuiteInterface):
    name = "shows"

    paths = {
        "get_trending": Path(
            "shows/trending",
            [TrendingShow],
            filters=COMMON_FILTERS | SHOWS_FILTERS,
            extended=["full"],
            pagination=True,
        )
    }

    def get_trending(self, **kwargs: Any) -> Iterable[TrendingShow]:
        return self.run("get_trending", **kwargs)


class ListsI(SuiteInterface):
    name = "lists"

    paths = {
        "get_trending": Path(
            "lists/trending", [ListResponse], extended=["full"], pagination=True
        ),
        "get_popular": Path(
            "lists/popular", [ListResponse], extended=["full"], pagination=True
        ),
    }

    def get_trending(self, **kwargs: Any) -> Iterable[ListResponse]:
        return self.run("get_trending", **kwargs)

    def get_popular(self, **kwargs: Any) -> Iterable[ListResponse]:
        return self.run("get_popular", **kwargs)


class NetworksI(SuiteInterface):
    name = "networks"

    paths = {"get_networks": Path("networks", [Network])}

    def get_networks(self, **kwargs: Any) -> List[Network]:
        return self.run("get_networks", **kwargs)
