from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Type, Union

from trakt.core.exceptions import ArgumentError
from trakt.core.models import Episode, Movie, Season, Show, TraktList
from trakt.core.paths.response_structs import Comment

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.abstract import AbstractApi
    from trakt.core.executors import Executor
    from trakt.core.paths.path import Path


class SuiteInterface:
    paths: Dict[str, Path] = {}
    client: AbstractApi
    executor_class: Type[Executor]
    name: str

    def __init__(self, client: AbstractApi, executor: Type[Executor]) -> None:
        self.client = client
        self.executor_class = executor

    def find_matching(self, name: Union[List[str], str]) -> List[Path]:
        poss_paths = self.paths.values()

        params = name.split(".") if isinstance(name, str) else name
        if params[0] == self.name:
            params = params[1:]

        alias = ".".join(params)
        return [p for p in poss_paths if p.does_match(alias)]

    def run(self, command: str, **kwargs: Any) -> Any:
        return self.run_path(path=self._get_path(command), **kwargs)

    def run_path(self, path: Path, **kwargs: Any) -> Any:
        return self.executor_class(self.client).run(path=path, **kwargs)

    def _get_path(self, command: str) -> Path:
        return self.paths[command]

    @staticmethod
    def _generic_get_id(
        item: Union[Movie, Episode, Show, Season, Comment, str, int]
    ) -> Union[int, str]:
        if isinstance(item, (int, str)):
            return item
        if isinstance(item, Comment):
            return item.id
        elif isinstance(item, (Movie, Episode, Show, Season, TraktList)):
            return item.ids["trakt"]
        else:
            raise ArgumentError("item: invalid id")
