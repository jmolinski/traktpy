from dataclasses import asdict
from typing import Any, Dict, Optional, Union

from trakt.core.decorators import auth_required
from trakt.core.exceptions import ArgumentError
from trakt.core.models import Episode, Movie
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    EpisodeCheckin,
    MovieCheckin,
    Sharing,
    Show,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import AuthRequiredValidator, List, Validator

AUTH_VALIDATOR: List[Validator] = [AuthRequiredValidator()]


class CheckinI(SuiteInterface):
    name = "checkin"

    paths = {
        "delete_active_checkins": Path(
            "checkin", {}, methods="DELETE", validators=AUTH_VALIDATOR
        ),
        "check_into_episode": Path(
            "checkin", EpisodeCheckin, methods="POST", validators=AUTH_VALIDATOR
        ),
        "check_into_movie": Path(
            "checkin", MovieCheckin, methods="POST", validators=AUTH_VALIDATOR
        ),
    }

    @auth_required
    def check_into(
        self,
        *,
        movie: Optional[Union[Movie, Dict[str, Any]]] = None,
        episode: Optional[Union[Episode, Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> Union[EpisodeCheckin, MovieCheckin]:
        if movie and episode:
            raise ArgumentError("you must provide exactly one of: [episode, movie]")

        if movie:
            return self.check_into_movie(movie, **kwargs)
        elif episode:
            return self.check_into_episode(episode, **kwargs)
        else:
            raise ArgumentError("you must provide exactly one of: [episode, movie]")

    def check_into_episode(
        self, episode: Union[Episode, Dict[str, Any]], **kwargs
    ) -> EpisodeCheckin:
        data = self._prepare_common_data(**kwargs)

        if isinstance(episode, Episode):
            episode = {"ids": {"trakt": episode.ids["trakt"]}}
        data["episode"] = episode

        if "show" in kwargs:
            show = kwargs["show"]
            if isinstance(show, Show):
                show = {"ids": {"trakt": show.ids["trakt"]}}
            data["show"] = show

        return self.run("check_into_episode", **kwargs, body=data)

    def check_into_movie(
        self, movie: Union[Movie, Dict[str, Any]], **kwargs
    ) -> MovieCheckin:
        data = self._prepare_common_data(**kwargs)

        if isinstance(movie, Movie):
            movie = {"ids": {"trakt": movie.ids["trakt"]}}
        data["movie"] = movie

        return self.run("check_into_movie", **kwargs, body=data)

    def _prepare_common_data(
        self, **kwargs: Any
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        d: Dict[str, Union[str, Dict[str, str]]] = {}

        if "sharing" in kwargs:
            if isinstance(kwargs["sharing"], Sharing):
                d["sharing"] = asdict(kwargs["sharing"])
            else:
                d["sharing"] = kwargs["sharing"]

        for f in ["message", "venue_id", "venue_name", "app_version", "app_date"]:
            if f in kwargs:
                v = kwargs[f]
                if v and isinstance(v, str):
                    d[f] = v

        return d

    def delete_active_checkins(self, **kwargs: Any) -> None:
        # TODO test delete method
        self.run("delete_active_checkins", **kwargs)
