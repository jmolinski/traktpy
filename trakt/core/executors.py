from typing import List

from trakt.core.abstract import AbstractApi
from trakt.core.restpaths import Path


class Executor:
    params: List[str]
    client: AbstractApi
    paths: List[Path]

    def __init__(self, client: AbstractApi, module: str) -> None:
        self.params = [module]
        self.client = client
        self.paths = []

    def __getattr__(self, param: str) -> "Executor":
        self.params.append(param)

        return self

    def __repr__(self) -> str:
        return f'Executor(params={".".join(self.params)})'

    def __call__(self, *args, **kwargs):
        return repr(self)

    def install(self, paths):
        if isinstance(paths, list):
            self.paths.extend(paths)
        else:
            self.paths.append(paths)
