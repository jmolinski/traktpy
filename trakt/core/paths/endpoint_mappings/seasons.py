from typing import Iterable, List, Union

from trakt.core.models import Comment, Episode, Season
from trakt.core.paths.endpoint_mappings.movies import (
    COMMENT_SORT_VALUES,
    LIST_SORT_VALUES,
    LIST_TYPE_VALUES,
)
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    RatingsSummary,
    SeasonEpisodeStats,
    Show,
    TraktList,
    User,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import PerArgValidator

ID_VALIDATOR = PerArgValidator("id", lambda i: isinstance(i, (int, str)))
SEASON_ID_VALIDATOR = PerArgValidator("season", lambda i: isinstance(i, int))


class SeasonsI(SuiteInterface):
    name = "seasons"

    paths = {
        "get_all_seasons": Path(
            "shows/!id/seasons",
            [Season],
            extended=["full", "episodes"],
            validators=[ID_VALIDATOR],
        ),
        "get_season": Path(
            "shows/!id/seasons/!season",
            [Episode],
            extended=["full", "episodes"],
            validators=[
                ID_VALIDATOR,
                SEASON_ID_VALIDATOR,
                PerArgValidator(
                    "translations",
                    lambda t: isinstance(t, str) and (t == "all" or len(t) == 2),
                ),
            ],
            qargs=["translations"],
        ),
        "get_comments": Path(
            "shows/!id/seasons/!season/comments/?sort",
            [Comment],
            validators=[
                ID_VALIDATOR,
                SEASON_ID_VALIDATOR,
                PerArgValidator("sort", lambda s: s in COMMENT_SORT_VALUES),
            ],
            pagination=True,
        ),
        "get_lists": Path(
            "shows/!id/seasons/!season/lists/?type/?sort",
            [TraktList],
            validators=[
                ID_VALIDATOR,
                SEASON_ID_VALIDATOR,
                PerArgValidator("type", lambda t: t in LIST_TYPE_VALUES),
                PerArgValidator("sort", lambda s: s in LIST_SORT_VALUES),
            ],
            pagination=True,
        ),
        "get_ratings": Path(
            "shows/!id/seasons/!season/ratings",
            RatingsSummary,
            validators=[ID_VALIDATOR, SEASON_ID_VALIDATOR],
        ),
        "get_stats": Path(
            "shows/!id/seasons/!season/stats",
            SeasonEpisodeStats,
            validators=[ID_VALIDATOR, SEASON_ID_VALIDATOR],
        ),
        "get_users_watching": Path(
            "shows/!id/seasons/!season/watching",
            [User],
            extended=["full"],
            validators=[ID_VALIDATOR, SEASON_ID_VALIDATOR],
        ),
    }

    def get_all_seasons(
        self, *, show: Union[Show, str, int], season: Union[Season, str, int], **kwargs
    ) -> List[Season]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        return self.run("get_all_seasons", **kwargs, id=id, season=season)

    def get_season(
        self, *, show: Union[Show, str, int], season: Union[Season, str, int], **kwargs
    ) -> List[Episode]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        return self.run("get_season", **kwargs, id=id, season=season)

    def get_comments(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        sort: str = "newest",
        **kwargs
    ) -> Iterable[Comment]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        return self.run("get_comments", **kwargs, sort=sort, id=id, season=season)

    def get_lists(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        type: str = "personal",
        sort: str = "popular",
        **kwargs
    ) -> Iterable[TraktList]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        return self.run(
            "get_lists", **kwargs, type=type, sort=sort, id=id, season=season
        )

    def get_ratings(
        self, *, show: Union[Show, str, int], season: Union[Season, str, int], **kwargs
    ) -> RatingsSummary:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        return self.run("get_ratings", **kwargs, id=id, season=season)

    def get_stats(
        self, *, show: Union[Show, str, int], season: Union[Season, str, int], **kwargs
    ) -> SeasonEpisodeStats:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        return self.run("get_stats", **kwargs, id=id, season=season)

    def get_users_watching(
        self, *, show: Union[Show, str, int], season: Union[Season, str, int], **kwargs
    ) -> List[User]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        return self.run("get_users_watching", **kwargs, id=id, season=season)
