import re
from typing import Any, List

from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import EpisodePremiere, MoviePremiere
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import (
    COMMON_FILTERS,
    SHOWS_FILTERS,
    AuthRequiredValidator,
    PerArgValidator,
    Validator,
)


class CalendarsI(SuiteInterface):
    name = "calendars"

    base_paths = {
        "get_shows": ["all/shows/?start_date/?days", [EpisodePremiere]],
        "get_my_shows": ["my/shows/?start_date/?days", [EpisodePremiere]],
        "get_new_shows": ["all/shows/new/?start_date/?days", [EpisodePremiere]],
        "get_my_new_shows": ["my/shows/new/?start_date/?days", [EpisodePremiere]],
        "get_season_premieres": [
            "all/shows/premieres/?start_date/?days",
            [EpisodePremiere],
        ],
        "get_my_season_premieres": [
            "my/shows/premieres/?start_date/?days",
            [EpisodePremiere],
        ],
        "get_movies": ["all/movies/?start_date/?days", [MoviePremiere]],
        "get_my_movies": ["my/movies/?start_date/?days", [MoviePremiere]],
        "get_dvd_releases": ["all/dvd/?start_date/?days", [MoviePremiere]],
        "get_my_dvd_releases": ["my/dvd/?start_date/?days", [MoviePremiere]],
    }

    COMMON_VALIDATORS: List[Validator] = [
        PerArgValidator("days", lambda t: isinstance(t, int)),
        PerArgValidator("start_date", lambda t: re.match(r"\d{4}-\d{2}-\d{2}", t)),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paths = {k: self._make_path(*r) for k, r in self.base_paths.items()}

    def _make_path(self, resource_path: str, return_type: Any) -> Path:
        extra_validators = [AuthRequiredValidator()] if "my/" in resource_path else []

        return Path(
            "calendars/" + resource_path,
            return_type,
            extended=["full"],
            filters=COMMON_FILTERS | SHOWS_FILTERS,
            validators=self.COMMON_VALIDATORS + extra_validators,  # type: ignore
        )

    def get_shows(self, **kwargs: Any) -> List[EpisodePremiere]:
        return self.run("get_shows", **kwargs)

    def get_my_shows(self, **kwargs: Any) -> List[EpisodePremiere]:
        return self.run("get_my_shows", **kwargs)

    def get_new_shows(self, **kwargs: Any) -> List[EpisodePremiere]:
        return self.run("get_new_shows", **kwargs)

    def get_my_new_shows(self, **kwargs: Any) -> List[EpisodePremiere]:
        return self.run("get_my_new_shows", **kwargs)

    def get_season_premieres(self, **kwargs: Any) -> List[EpisodePremiere]:
        return self.run("get_season_premieres", **kwargs)

    def get_my_season_premieres(self, **kwargs: Any) -> List[EpisodePremiere]:
        return self.run("get_my_season_premieres", **kwargs)

    def get_movies(self, **kwargs: Any) -> List[MoviePremiere]:
        return self.run("get_movies", **kwargs)

    def get_my_movies(self, **kwargs: Any) -> List[MoviePremiere]:
        return self.run("get_my_movies", **kwargs)

    def get_dvd_releases(self, **kwargs: Any) -> List[MoviePremiere]:
        return self.run("get_dvd_releases", **kwargs)

    def get_my_dvd_releases(self, **kwargs: Any) -> List[MoviePremiere]:
        return self.run("get_my_dvd_releases", **kwargs)
