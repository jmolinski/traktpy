from typing import Any, Dict, Iterable, List, Optional, Union

from trakt.core.models import Comment
from trakt.core.paths.endpoint_mappings.movies import (
    COMMENT_SORT_VALUES,
    LIST_SORT_VALUES,
    LIST_TYPE_VALUES,
    PERIOD_VALUES,
)
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    Alias,
    AnticipatedShow,
    CastCrewList,
    Episode,
    RatingsSummary,
    Show,
    ShowCollectionProgress,
    ShowStats,
    ShowTranslation,
    ShowWatchedProgress,
    ShowWithStats,
    TraktList,
    TrendingShow,
    UpdatedShow,
    User,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import (
    COMMON_FILTERS,
    SHOWS_FILTERS,
    AuthRequiredValidator,
    PerArgValidator,
    Validator,
    is_date,
)

ID_VALIDATOR = PerArgValidator("id", lambda i: isinstance(i, (int, str)))

PROGRESS_VALIDATORS: List[Validator] = [
    AuthRequiredValidator(),
    ID_VALIDATOR,
    PerArgValidator("hidden", lambda t: isinstance(t, bool)),
    PerArgValidator("specials", lambda t: isinstance(t, bool)),
    PerArgValidator("count_specials", lambda t: isinstance(t, bool)),
    PerArgValidator("last_activity", lambda t: t in {"collected", "watched"}),
]


class ShowsI(SuiteInterface):
    name = "shows"

    base_paths = {
        "get_trending": ["trending", [TrendingShow]],
        "get_popular": ["popular", [Show]],
        "get_most_played": ["played/?period", [ShowWithStats]],
        "get_most_watched": ["watched/?period", [ShowWithStats]],
        "get_most_collected": ["collected/?period", [ShowWithStats]],
        "get_most_anticipated": ["anticipated", [AnticipatedShow]],
    }

    paths = {
        "get_recently_updated": Path(
            "shows/updates/?start_date",
            [UpdatedShow],
            extended=["full"],
            pagination=True,
            validators=[PerArgValidator("start_date", is_date)],
        ),
        "get_summary": Path(
            "shows/!id", Show, extended=["full"], validators=[ID_VALIDATOR]
        ),
        "get_aliases": Path("shows/!id/aliases", [Alias], validators=[ID_VALIDATOR]),
        "get_translations": Path(
            "shows/!id/translations/?language",
            [ShowTranslation],
            validators=[
                ID_VALIDATOR,
                PerArgValidator(
                    "language", lambda c: isinstance(c, str) and len(c) == 2
                ),
            ],
        ),
        "get_comments": Path(
            "shows/!id/comments/?sort",
            [Comment],
            validators=[
                ID_VALIDATOR,
                PerArgValidator("sort", lambda s: s in COMMENT_SORT_VALUES),
            ],
            pagination=True,
        ),
        "get_lists": Path(
            "shows/!id/lists/?type/?sort",
            [TraktList],
            validators=[
                ID_VALIDATOR,
                PerArgValidator("type", lambda t: t in LIST_TYPE_VALUES),
                PerArgValidator("sort", lambda s: s in LIST_SORT_VALUES),
            ],
            pagination=True,
        ),
        "get_collection_progress": Path(
            "shows/!id/progress/collection",
            ShowCollectionProgress,
            validators=PROGRESS_VALIDATORS,
            qargs=["hidden", "specials", "count_specials", "last_activity"],
        ),
        "get_watched_progress": Path(
            "shows/!id/progress/watched",
            ShowWatchedProgress,
            validators=PROGRESS_VALIDATORS,
            qargs=["hidden", "specials", "count_specials", "last_activity"],
        ),
        "get_people": Path(
            "shows/!id/people",
            CastCrewList,
            extended=["full"],
            validators=[ID_VALIDATOR],
        ),
        "get_ratings": Path(
            "shows/!id/ratings", RatingsSummary, validators=[ID_VALIDATOR]
        ),
        "get_related": Path(
            "shows/!id/related",
            [Show],
            extended=["full"],
            pagination=True,
            validators=[ID_VALIDATOR],
        ),
        "get_stats": Path("shows/!id/stats", ShowStats, validators=[ID_VALIDATOR]),
        "get_users_watching": Path(
            "shows/!id/watching", [User], extended=["full"], validators=[ID_VALIDATOR]
        ),
        "get_next_episode": Path(
            "shows/!id/next_episode",
            Union[Episode, Dict[str, Any]],
            extended=["full"],
            validators=[ID_VALIDATOR],
        ),
        "get_last_episode": Path(
            "shows/!id/last_episode",
            Union[Episode, Dict[str, Any]],
            extended=["full"],
            validators=[ID_VALIDATOR],
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
            self.name + "/" + resource_path,
            return_type,
            extended=["full"],
            filters=COMMON_FILTERS | SHOWS_FILTERS,
            pagination=True,
            validators=extra_validators,
        )

    def get_trending(self, **kwargs) -> Iterable[TrendingShow]:
        return self.run("get_trending", **kwargs)

    def get_popular(self, **kwargs) -> Iterable[Show]:
        return self.run("get_popular", **kwargs)

    def get_most_played(
        self, *, period: str = "weekly", **kwargs
    ) -> Iterable[ShowWithStats]:
        return self.run("get_most_played", **kwargs, period=period)

    def get_most_watched(
        self, *, period: str = "weekly", **kwargs
    ) -> Iterable[ShowWithStats]:
        return self.run("get_most_watched", **kwargs, period=period)

    def get_most_collected(
        self, *, period: str = "weekly", **kwargs
    ) -> Iterable[ShowWithStats]:
        return self.run("get_most_collected", **kwargs, period=period)

    def get_most_anticipated(self, **kwargs) -> Iterable[AnticipatedShow]:
        return self.run("get_most_anticipated", **kwargs)

    def get_recently_updated(
        self, *, start_date: Optional[str] = None, **kwargs
    ) -> Iterable[UpdatedShow]:
        return self.run("get_recently_updated", **kwargs, start_date=start_date)

    def get_summary(self, *, show: Union[Show, str, int], **kwargs) -> Iterable[Show]:
        id = self._generic_get_id(show)
        return self.run("get_summary", **kwargs, id=id)

    def get_aliases(self, *, show: Union[Show, str, int], **kwargs) -> List[Alias]:
        id = self._generic_get_id(show)
        return self.run("get_aliases", **kwargs, id=id)

    def get_translations(
        self, *, show: Union[Show, str, int], language: Optional[str] = None, **kwargs
    ) -> List[ShowTranslation]:
        extra_kwargs = {"id": self._generic_get_id(show)}
        if language:
            extra_kwargs["language"] = language

        return self.run("get_translations", **kwargs, **extra_kwargs)

    def get_comments(
        self, *, show: Union[Show, str, int], sort: str = "newest", **kwargs
    ) -> Iterable[Comment]:
        id = self._generic_get_id(show)
        return self.run("get_comments", **kwargs, sort=sort, id=id)

    def get_lists(
        self,
        *,
        show: Union[Show, str, int],
        type: str = "personal",
        sort: str = "popular",
        **kwargs
    ) -> Iterable[TraktList]:
        id = self._generic_get_id(show)
        return self.run("get_lists", **kwargs, type=type, sort=sort, id=id)

    def get_collection_progress(
        self,
        *,
        show: Union[Show, str, int],
        hidden: bool = False,
        specials: bool = False,
        count_specials: bool = True,
        **kwargs
    ) -> ShowCollectionProgress:
        return self.run(
            "get_collection_progress",
            **kwargs,
            id=self._generic_get_id(show),
            hidden=hidden,
            specials=specials,
            count_specials=count_specials
        )

    def get_watched_progress(
        self,
        *,
        show: Union[Show, str, int],
        hidden: bool = False,
        specials: bool = False,
        count_specials: bool = True,
        **kwargs
    ) -> ShowCollectionProgress:
        return self.run(
            "get_watched_progress",
            **kwargs,
            id=self._generic_get_id(show),
            hidden=hidden,
            specials=specials,
            count_specials=count_specials
        )

    def get_people(self, *, show: Union[Show, str, int], **kwargs) -> CastCrewList:
        return self.run("get_people", **kwargs, id=self._generic_get_id(show))

    def get_ratings(self, *, show: Union[Show, str, int], **kwargs) -> RatingsSummary:
        return self.run("get_ratings", **kwargs, id=self._generic_get_id(show))

    def get_related(self, *, show: Union[Show, str, int], **kwargs) -> Iterable[Show]:
        return self.run("get_related", **kwargs, id=self._generic_get_id(show))

    def get_stats(self, *, show: Union[Show, str, int], **kwargs) -> ShowStats:
        return self.run("get_stats", **kwargs, id=self._generic_get_id(show))

    def get_users_watching(
        self, *, show: Union[Show, str, int], **kwargs
    ) -> List[User]:
        return self.run("get_users_watching", **kwargs, id=self._generic_get_id(show))

    def get_next_episode(
        self, *, show: Union[Show, str, int], **kwargs
    ) -> Optional[Episode]:
        resp, code = self.run(
            "get_next_episode",
            **kwargs,
            id=self._generic_get_id(show),
            return_code=True
        )

        return None if code == 204 else resp

    def get_last_episode(
        self, *, show: Union[Show, str, int], **kwargs
    ) -> Optional[Episode]:
        resp, code = self.run(
            "get_last_episode",
            **kwargs,
            id=self._generic_get_id(show),
            return_code=True
        )

        return None if code == 204 else resp
