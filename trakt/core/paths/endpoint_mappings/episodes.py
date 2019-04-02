from typing import Iterable, List, Union

from trakt.core.models import Comment, Episode, Season
from trakt.core.paths.endpoint_mappings.movies import (
    COMMENT_SORT_VALUES,
    LIST_SORT_VALUES,
    LIST_TYPE_VALUES,
)
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    EpisodeTranslation,
    RatingsSummary,
    SeasoneEpisodeStats,
    Show,
    TraktList,
    User,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import PerArgValidator

ID_VALIDATOR = PerArgValidator("id", lambda i: isinstance(i, (int, str)))
SEASON_ID_VALIDATOR = PerArgValidator("season", lambda i: isinstance(i, int))
EPISODE_ID_VALIDATOR = PerArgValidator("season", lambda i: isinstance(i, int))


class EpisodesI(SuiteInterface):
    name = "episodes"

    paths = {
        "get_episode": Path(
            "shows/!id/seasons/!season/episodes/!episode",
            Episode,
            extended=["full"],
            validators=[ID_VALIDATOR, SEASON_ID_VALIDATOR, EPISODE_ID_VALIDATOR],
        ),
        "get_translations": Path(
            "shows/!id/seasons/!season/comments/episodes/!episode/translations/?language",
            [EpisodeTranslation],
            validators=[
                ID_VALIDATOR,
                SEASON_ID_VALIDATOR,
                EPISODE_ID_VALIDATOR,
                PerArgValidator("language", lambda s: isinstance(s, str)),
            ],
            pagination=True,
        ),
        "get_comments": Path(
            "shows/!id/seasons/!season/comments/episodes/!episode/?sort",
            [Comment],
            validators=[
                ID_VALIDATOR,
                SEASON_ID_VALIDATOR,
                EPISODE_ID_VALIDATOR,
                PerArgValidator("sort", lambda s: s in COMMENT_SORT_VALUES),
            ],
            pagination=True,
        ),
        "get_lists": Path(
            "shows/!id/seasons/!season/episodes/!episode/lists/?type/?sort",
            [TraktList],
            validators=[
                ID_VALIDATOR,
                SEASON_ID_VALIDATOR,
                EPISODE_ID_VALIDATOR,
                PerArgValidator("type", lambda t: t in LIST_TYPE_VALUES),
                PerArgValidator("sort", lambda s: s in LIST_SORT_VALUES),
            ],
            pagination=True,
        ),
        "get_ratings": Path(
            "shows/!id/seasons/!season/episodes/!episode/ratings",
            RatingsSummary,
            validators=[ID_VALIDATOR, SEASON_ID_VALIDATOR, EPISODE_ID_VALIDATOR],
        ),
        "get_stats": Path(
            "shows/!id/seasons/!season/episodes/!episode/stats",
            SeasoneEpisodeStats,
            validators=[ID_VALIDATOR, SEASON_ID_VALIDATOR, EPISODE_ID_VALIDATOR],
        ),
        "get_users_watching": Path(
            "shows/!id/seasons/!season/episodes/!episode/watching",
            [User],
            extended=["full"],
            validators=[ID_VALIDATOR, SEASON_ID_VALIDATOR, EPISODE_ID_VALIDATOR],
        ),
    }

    def get_season(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        episode: Union[Episode, int, str],
        **kwargs
    ) -> Season:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        episode = self._generic_get_id(episode)
        return self.run("get_season", **kwargs, id=id, season=season, episode=episode)

    def get_comments(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        episode: Union[Episode, int, str],
        sort: str = "newest",
        **kwargs
    ) -> Iterable[Comment]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        episode = self._generic_get_id(episode)
        return self.run(
            "get_comments", **kwargs, sort=sort, id=id, season=season, episode=episode
        )

    def get_translations(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        episode: Union[Episode, int, str],
        sort: str = "newest",
        **kwargs
    ) -> Iterable[Comment]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        episode = self._generic_get_id(episode)
        return self.run(
            "get_comments", **kwargs, sort=sort, id=id, season=season, episode=episode
        )

    def get_lists(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        episode: Union[Episode, int, str],
        type: str = "personal",
        sort: str = "popular",
        **kwargs
    ) -> Iterable[TraktList]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        episode = self._generic_get_id(episode)
        return self.run(
            "get_lists",
            **kwargs,
            type=type,
            sort=sort,
            id=id,
            season=season,
            episode=episode
        )

    def get_ratings(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        episode: Union[Episode, int, str],
        **kwargs
    ) -> RatingsSummary:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        episode = self._generic_get_id(episode)
        return self.run("get_ratings", **kwargs, id=id, season=season, episode=episode)

    def get_stats(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        episode: Union[Episode, int, str],
        **kwargs
    ) -> SeasoneEpisodeStats:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        episode = self._generic_get_id(episode)
        return self.run("get_stats", **kwargs, id=id, season=season, episode=episode)

    def get_users_watching(
        self,
        *,
        show: Union[Show, str, int],
        season: Union[Season, str, int],
        episode: Union[Episode, int, str],
        **kwargs
    ) -> List[User]:
        id = self._generic_get_id(show)
        season = self._generic_get_id(season)
        episode = self._generic_get_id(episode)
        return self.run(
            "get_users_watching", **kwargs, id=id, season=season, episode=episode
        )
