from typing import Any, Iterable, List, Optional

from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    AnticipatedMovie,
    BoxOffice,
    Movie,
    MovieStats,
    TrendingMovie,
    UpdatedMovie,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import (
    COMMON_FILTERS,
    PerArgValidator,
    Validator,
    is_date,
)

PERIOD_VALUES = {"weekly", "monthly", "yearly", "all"}


class MoviesI(SuiteInterface):
    name = "movies"

    base_paths = {
        "get_trending": ["trending", [TrendingMovie]],
        "get_popular": ["popular", [Movie]],
        "get_most_played": ["played/?period", [MovieStats]],
        "get_most_watched": ["watched/?period", [MovieStats]],
        "get_most_collected": ["collected/?period", [MovieStats]],
        "get_most_anticipated": ["anticipated", [AnticipatedMovie]],
    }

    paths = {
        "get_box_office": Path("movies/boxoffice", [BoxOffice], extended=["full"]),
        "get_recently_updated": Path(
            "movies/updates/?start_date",
            [UpdatedMovie],
            extended=["full"],
            pagination=True,
            validators=[PerArgValidator("start_date", is_date)],
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for k, r in self.base_paths.items():
            self.paths[k] = self._make_path(*r)

    def _make_path(self, resource_path: str, return_type: Any) -> Path:
        extra_validators: List[Validator] = []
        if "?period" in resource_path:
            extra_validators.append(
                PerArgValidator("period", lambda p: p in PERIOD_VALUES)
            )

        return Path(
            "calendars/" + resource_path,
            return_type,
            extended=["full"],
            filters=COMMON_FILTERS,
            pagination=True,
            validators=extra_validators,
        )

    def get_trending(self, **kwargs) -> Iterable[TrendingMovie]:
        return self.run("get_trending", **kwargs)

    def get_popular(self, **kwargs) -> Iterable[Movie]:
        return self.run("get_popular", **kwargs)

    def get_most_played(self, period: str = "weekly", **kwargs) -> Iterable[MovieStats]:
        return self.run("get_most_played", **kwargs, period=period)

    def get_most_watched(
        self, period: str = "weekly", **kwargs
    ) -> Iterable[MovieStats]:
        return self.run("get_most_watched", **kwargs, period=period)

    def get_most_collected(
        self, period: str = "weekly", **kwargs
    ) -> Iterable[MovieStats]:
        return self.run("get_most_collected", **kwargs, period=period)

    def get_most_anticipated(self, **kwargs) -> Iterable[AnticipatedMovie]:
        return self.run("get_most_anticipated", **kwargs)

    def get_box_office(self, **kwargs) -> List[BoxOffice]:
        return self.run("get_box_office", **kwargs)

    def get_recently_updated(
        self, *, start_date: Optional[str] = None, **kwargs
    ) -> Iterable[UpdatedMovie]:
        return self.run("get_recently_updated", **kwargs, start_date=start_date)
