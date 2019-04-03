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
from trakt.core.paths.validators import AuthRequiredValidator, PerArgValidator

MESSAGE_VALIDATOR = PerArgValidator("message", lambda m: isinstance(m, str))


class CheckinI(SuiteInterface):
    name = "checkin"

    paths = {
        "delete_active_checkins": Path(
            "checkin", {}, methods="DELETE", validators=[AuthRequiredValidator()]
        ),
        "check_into_episode": Path(
            "checkin",
            EpisodeCheckin,
            methods="POST",
            validators=[AuthRequiredValidator(), MESSAGE_VALIDATOR],
        ),
        "check_into_movie": Path(
            "checkin",
            MovieCheckin,
            methods="POST",
            validators=[AuthRequiredValidator(), MESSAGE_VALIDATOR],
        ),
    }

    @auth_required
    def check_into(
        self,
        *,
        movie: Optional[Union[Movie, Dict[str, Any]]] = None,
        episode: Optional[Union[Episode, Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> Union[EpisodeCheckin, MovieCheckin]:
        if movie and episode:
            raise ArgumentError("you must provide exactly one of: [episode, movie]")

        if movie:
            return self.check_into_movie(movie=movie, **kwargs)
        elif episode:
            return self.check_into_episode(episode=episode, **kwargs)
        else:
            raise ArgumentError("you must provide exactly one of: [episode, movie]")

    def check_into_episode(
        self,
        *,
        episode: Union[Episode, Dict[str, Any]],
        message: Optional[str] = None,
        sharing: Optional[Union[Sharing, Dict[str, str]]] = None,
        **kwargs,
    ) -> EpisodeCheckin:
        data: Dict[str, Any] = self._prepare_common_data(
            **kwargs, message=message, sharing=sharing
        )

        if isinstance(episode, Episode):
            episode = {"ids": {"trakt": episode.ids["trakt"]}}
        data["episode"] = episode

        if "show" in kwargs:
            show = kwargs["show"]
            if isinstance(show, Show):
                data["show"] = {"ids": {"trakt": show.ids["trakt"]}}
            elif isinstance(show, dict):
                data["show"] = show
            else:
                raise ArgumentError("show: invalid argument value")

        return self.run("check_into_episode", **data, body=data)

    def check_into_movie(
        self,
        *,
        movie: Union[Movie, Dict[str, Any]],
        message: Optional[str] = None,
        sharing: Optional[Union[Sharing, Dict[str, str]]] = None,
        **kwargs,
    ) -> MovieCheckin:
        data = self._prepare_common_data(**kwargs, message=message, sharing=sharing)

        if isinstance(movie, Movie):
            movie = {"ids": {"trakt": movie.ids["trakt"]}}
        data["movie"] = movie

        return self.run("check_into_movie", **data, body=data)

    def _prepare_common_data(
        self, **kwargs: Any
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        d: Dict[str, Union[str, Dict[str, str]]] = {}

        if "sharing" in kwargs and kwargs["sharing"] is not None:
            if isinstance(kwargs["sharing"], Sharing):
                d["sharing"] = asdict(kwargs["sharing"])
            elif isinstance(kwargs["sharing"], dict):
                d["sharing"] = kwargs["sharing"]
            else:
                raise ArgumentError("sharing: invalid argument value")

        for f in ["message", "venue_id", "venue_name", "app_version", "app_date"]:
            if f in kwargs:
                v = kwargs[f]
                if v is not None:
                    d[f] = v

        return d

    def delete_active_checkins(self, **kwargs: Any) -> None:
        # TODO test delete method
        self.run("delete_active_checkins", **kwargs)
