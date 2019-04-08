from typing import Any, Dict, Optional, Union

from trakt.core.exceptions import ArgumentError
from trakt.core.models import Episode, Movie
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import EpisodeScrobble, MovieScrobble, Show
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import AuthRequiredValidator, PerArgValidator

PROGRESS_VALIDATOR = PerArgValidator(
    "progress", lambda p: isinstance(p, (int, float)) and 100 >= p >= 0
)


class ScrobbleI(SuiteInterface):
    name = "scrobble"

    base_paths = {
        "start_scrobble_movie": ["start", MovieScrobble],
        "start_scrobble_episode": ["start", EpisodeScrobble],
        "pause_scrobble_movie": ["pause", MovieScrobble],
        "pause_scrobble_episode": ["pause", EpisodeScrobble],
        "stop_scrobble_movie": ["stop", MovieScrobble],
        "stop_scrobble_episode": ["stop", EpisodeScrobble],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for k, r in self.base_paths.items():
            self.paths[k] = self._make_path(*r)

    def _make_path(self, resource_path: str, return_type: Any) -> Path:
        return Path(
            self.name + "/" + resource_path,
            return_type,
            validators=[AuthRequiredValidator(), PROGRESS_VALIDATOR],
        )

    def start_scrobble(
        self,
        *,
        movie: Optional[Union[Movie, Dict[str, Any]]] = None,
        episode: Optional[Union[Episode, Dict[str, Any]]] = None,
        show: Optional[Union[Show, Dict[str, Any]]] = None,
        progress: float,
        **kwargs: Any,
    ) -> Union[MovieScrobble, EpisodeScrobble]:
        if movie and episode:
            raise ArgumentError("you must provide exactly one of: [episode, movie]")

        if movie:
            return self.start_scrobble_movie(movie=movie, progress=progress, **kwargs)
        elif episode:
            return self.start_scrobble_episode(
                episode=episode, show=show, progress=progress, **kwargs
            )
        else:
            raise ArgumentError("you must provide exactly one of: [episode, movie]")

    def start_scrobble_movie(
        self, *, movie: Union[Movie, Dict[str, Any]], progress: float, **kwargs
    ) -> MovieScrobble:
        data = self._prepare_movie_data(movie=movie, progress=progress)
        return self.run("start_scrobble_movie", **kwargs, body=data, progress=progress)

    def start_scrobble_episode(
        self, *, episode: Union[Episode, Dict[str, Any]], progress: float, **kwargs
    ) -> EpisodeScrobble:
        data = self._prepare_episode_data(episode, progress, show=kwargs.get("show"))
        return self.run(
            "start_scrobble_episode", **kwargs, body=data, progress=progress
        )

    def pause_scrobble(
        self,
        *,
        movie: Optional[Union[Movie, Dict[str, Any]]] = None,
        episode: Optional[Union[Episode, Dict[str, Any]]] = None,
        show: Optional[Union[Show, Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> Union[MovieScrobble, EpisodeScrobble]:
        if movie and episode:
            raise ArgumentError("you must provide exactly one of: [episode, movie]")

        if movie:
            return self.pause_scrobble_movie(movie=movie, **kwargs)
        elif episode:
            return self.pause_scrobble_episode(episode=episode, show=show, **kwargs)
        else:
            raise ArgumentError("you must provide exactly one of: [episode, movie]")

    def pause_scrobble_movie(
        self, *, movie: Union[Movie, Dict[str, Any]], progress: float, **kwargs
    ) -> MovieScrobble:
        data = self._prepare_movie_data(movie=movie, progress=progress)
        return self.run("pause_scrobble_movie", **kwargs, body=data, progress=progress)

    def pause_scrobble_episode(
        self, *, episode: Union[Episode, Dict[str, Any]], progress: float, **kwargs
    ) -> EpisodeScrobble:
        data = self._prepare_episode_data(episode, progress, show=kwargs.get("show"))
        return self.run(
            "pause_scrobble_episode", **kwargs, body=data, progress=progress
        )

    def stop_scrobble(
        self,
        *,
        movie: Optional[Union[Movie, Dict[str, Any]]] = None,
        episode: Optional[Union[Episode, Dict[str, Any]]] = None,
        show: Optional[Union[Show, Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> Union[MovieScrobble, EpisodeScrobble]:
        if movie and episode:
            raise ArgumentError("you can either provide episode or movie, not both")

        if movie:
            return self.stop_scrobble_movie(movie=movie, **kwargs)
        elif episode:
            return self.stop_scrobble_episode(episode=episode, show=show, **kwargs)
        else:
            raise ArgumentError("missing both episode and movie arguments")

    def stop_scrobble_movie(
        self, *, movie: Union[Movie, Dict[str, Any]], progress: float, **kwargs
    ) -> MovieScrobble:
        data = self._prepare_movie_data(movie=movie, progress=progress)
        return self.run("stop_scrobble_movie", **kwargs, body=data, progress=progress)

    def stop_scrobble_episode(
        self, *, episode: Union[Episode, Dict[str, Any]], progress: float, **kwargs
    ) -> EpisodeScrobble:
        data = self._prepare_episode_data(episode, progress, show=kwargs.get("show"))
        return self.run("stop_scrobble_episode", **kwargs, body=data, progress=progress)

    def _prepare_episode_data(
        self,
        episode: Union[Episode, Dict[str, Any]],
        progress: float,
        show: Optional[Union[Show, int, str]] = None,
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {"progress": progress}

        if isinstance(episode, Episode):
            episode = {"ids": {"trakt": self._generic_get_id(episode)}}
        data["episode"] = episode

        if show:
            if isinstance(show, Show):
                data["show"] = {"ids": {"trakt": self._generic_get_id(show)}}
            else:
                data["show"] = show

        return data

    def _prepare_movie_data(
        self, progress: float, movie: Union[Movie, Dict[str, Any]]
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {"progress": progress}

        if isinstance(movie, Movie):
            data["movie"] = {"ids": {"trakt": self._generic_get_id(movie)}}
        else:
            data["movie"] = movie

        return data
