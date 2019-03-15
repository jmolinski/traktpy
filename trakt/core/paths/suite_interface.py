from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Type, Union

if TYPE_CHECKING:
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
        return self.executor_class(self.client).run(path=self.paths[command], **kwargs)
