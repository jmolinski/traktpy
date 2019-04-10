from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Union

from trakt.core.models import Comment
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    Alias,
    AnticipatedMovie,
    BoxOffice,
    CastCrewList,
    Movie,
    MovieRelease,
    MovieStats,
    MovieTranslation,
    MovieWithStats,
    RatingsSummary,
    TraktList,
    TrendingMovie,
    UpdatedMovie,
    User,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import (
    COMMON_FILTERS,
    PerArgValidator,
    Validator,
    is_date,
)

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.executors import PaginationIterator

PERIOD_VALUES = {"weekly", "monthly", "yearly", "all"}
COMMENT_SORT_VALUES = {"newest", "oldest", "likes", "replies"}
LIST_TYPE_VALUES = {"personal", "all", "official", "watchlist"}
LIST_SORT_VALUES = {"popular", "likes", "comments", "items", "added", "updated"}


class MoviesI(SuiteInterface):
    name = "movies"

    base_paths = {
        "get_trending": ["trending", [TrendingMovie]],
        "get_popular": ["popular", [Movie]],
        "get_most_played": ["played/?period", [MovieWithStats]],
        "get_most_watched": ["watched/?period", [MovieWithStats]],
        "get_most_collected": ["collected/?period", [MovieWithStats]],
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
        "get_summary": Path("movies/!id", Movie, extended=["full"]),
        "get_aliases": Path("movies/!id/aliases", [Alias]),
        "get_releases": Path(
            "movies/!id/releases/?country",
            [MovieRelease],
            validators=[
                PerArgValidator("country", lambda c: isinstance(c, str) and len(c) == 2)
            ],
        ),
        "get_translations": Path(
            "movies/!id/translations/?language",
            [MovieTranslation],
            validators=[
                PerArgValidator(
                    "language", lambda c: isinstance(c, str) and len(c) == 2
                )
            ],
        ),
        "get_comments": Path(
            "movies/!id/comments/?sort",
            [Comment],
            validators=[PerArgValidator("sort", lambda s: s in COMMENT_SORT_VALUES)],
            pagination=True,
        ),
        "get_lists": Path(
            "movies/!id/lists/?type/?sort",
            [TraktList],
            validators=[
                PerArgValidator("type", lambda t: t in LIST_TYPE_VALUES),
                PerArgValidator("sort", lambda s: s in LIST_SORT_VALUES),
            ],
            pagination=True,
        ),
        "get_people": Path("movies/!id/people", CastCrewList, extended=["full"]),
        "get_ratings": Path("movies/!id/ratings", RatingsSummary),
        "get_related": Path(
            "movies/!id/related", [Movie], extended=["full"], pagination=True
        ),
        "get_stats": Path("movies/!id/stats", MovieStats),
        "get_users_watching": Path("movies/!id/watching", [User], extended=["full"]),
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
            self.name + "/" + resource_path,
            return_type,
            extended=["full"],
            filters=COMMON_FILTERS,
            pagination=True,
            validators=extra_validators,
        )

    def get_trending(self, **kwargs) -> PaginationIterator[TrendingMovie]:
        return self.run("get_trending", **kwargs)

    def get_popular(self, **kwargs) -> PaginationIterator[Movie]:
        return self.run("get_popular", **kwargs)

    def get_most_played(
        self, *, period: str = "weekly", **kwargs
    ) -> PaginationIterator[MovieWithStats]:
        return self.run("get_most_played", **kwargs, period=period)

    def get_most_watched(
        self, *, period: str = "weekly", **kwargs
    ) -> PaginationIterator[MovieWithStats]:
        return self.run("get_most_watched", **kwargs, period=period)

    def get_most_collected(
        self, *, period: str = "weekly", **kwargs
    ) -> PaginationIterator[MovieWithStats]:
        return self.run("get_most_collected", **kwargs, period=period)

    def get_most_anticipated(self, **kwargs) -> PaginationIterator[AnticipatedMovie]:
        return self.run("get_most_anticipated", **kwargs)

    def get_box_office(self, **kwargs) -> List[BoxOffice]:
        return self.run("get_box_office", **kwargs)

    def get_recently_updated(
        self, *, start_date: Optional[str] = None, **kwargs
    ) -> PaginationIterator[UpdatedMovie]:
        return self.run("get_recently_updated", **kwargs, start_date=start_date)

    def get_summary(self, *, movie: Union[Movie, str, int], **kwargs) -> Movie:
        movie_id = self._get_movie_id(movie)
        return self.run("get_summary", **kwargs, id=movie_id)

    def get_aliases(self, *, movie: Union[Movie, str, int], **kwargs) -> List[Alias]:
        movie_id = self._get_movie_id(movie)
        return self.run("get_aliases", **kwargs, id=movie_id)

    def get_releases(
        self, *, movie: Union[Movie, str, int], country: Optional[str] = None, **kwargs
    ) -> List[MovieRelease]:
        extra_kwargs = {"id": self._get_movie_id(movie)}
        if country:
            extra_kwargs["country"] = country

        return self.run("get_releases", **kwargs, **extra_kwargs)

    def get_translations(
        self, *, movie: Union[Movie, str, int], language: Optional[str] = None, **kwargs
    ) -> List[MovieTranslation]:
        extra_kwargs = {"id": self._get_movie_id(movie)}
        if language:
            extra_kwargs["language"] = language

        return self.run("get_translations", **kwargs, **extra_kwargs)

    def get_comments(
        self, *, movie: Union[Movie, str, int], sort: str = "newest", **kwargs
    ) -> PaginationIterator[Comment]:
        movie_id = self._get_movie_id(movie)
        return self.run("get_comments", **kwargs, sort=sort, id=movie_id)

    def get_lists(
        self,
        *,
        movie: Union[Movie, str, int],
        type: str = "personal",
        sort: str = "popular",
        **kwargs
    ) -> PaginationIterator[TraktList]:
        movie_id = self._get_movie_id(movie)
        return self.run("get_lists", **kwargs, type=type, sort=sort, id=movie_id)

    def get_people(self, *, movie: Union[Movie, str, int], **kwargs) -> CastCrewList:
        return self.run("get_people", **kwargs, id=self._get_movie_id(movie))

    def get_ratings(self, *, movie: Union[Movie, str, int], **kwargs) -> RatingsSummary:
        return self.run("get_ratings", **kwargs, id=self._get_movie_id(movie))

    def get_related(
        self, *, movie: Union[Movie, str, int], **kwargs
    ) -> PaginationIterator[Movie]:
        return self.run("get_related", **kwargs, id=self._get_movie_id(movie))

    def get_stats(self, *, movie: Union[Movie, str, int], **kwargs) -> MovieStats:
        return self.run("get_stats", **kwargs, id=self._get_movie_id(movie))

    def get_users_watching(
        self, *, movie: Union[Movie, str, int], **kwargs
    ) -> List[User]:
        return self.run("get_users_watching", **kwargs, id=self._get_movie_id(movie))

    def _get_movie_id(self, movie: Union[Movie, str, int]) -> str:
        return str(self._generic_get_id(movie))
