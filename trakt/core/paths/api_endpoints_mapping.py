import re
from typing import Any, Iterable, List

from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    Certification,
    Country,
    Genre,
    Language,
    SeasonPremiere,
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
        ret = self.run("get_countries", type=type, **kwargs)
        return ret


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
        ret = self.run("get_genres", type=type, **kwargs)
        return ret


class LanguagesI(SuiteInterface):
    name = "languages"

    paths = {
        "get_languages": Path(
            "languages/!type", [Language], validators=[TYPE_MOVIES_SHOWS]
        )
    }

    def get_languages(self, *, type: str, **kwargs: Any) -> List[Language]:
        ret = self.run("get_languages", type=type, **kwargs)
        return ret


class CalendarsI(SuiteInterface):
    name = "calendars"

    paths = {
        "get_season_premieres": Path(
            "calendars/all/shows/premieres/?start_date/?days",
            [SeasonPremiere],
            validators=[
                PerArgValidator("days", lambda t: isinstance(t, int)),
                PerArgValidator(
                    "start_date", lambda t: re.match(r"\d{4}-\d{2}-\d{2}", t)
                ),
            ],
            filters=COMMON_FILTERS | SHOWS_FILTERS,
            extended=["full"],
        )
    }

    def get_season_premieres(self, **kwargs: Any) -> List[SeasonPremiere]:
        ret = self.run("get_season_premieres", **kwargs)
        return ret


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
        ret = self.run("get_trending", **kwargs)
        return ret
