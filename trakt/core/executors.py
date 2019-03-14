from typing import Any, List, Optional, Union

from trakt.core import json_parser
from trakt.core.abstract import AbstractApi, AbstractSuiteInterface
from trakt.core.exceptions import ClientError
from trakt.core.paths.path import Path


class Executor:
    params: List[str]
    client: AbstractApi
    paths: List[Path]
    path_suites: List[AbstractSuiteInterface]

    def __init__(
        self, client: AbstractApi, params: Union[List[str], str, None] = None
    ) -> None:
        if isinstance(params, str):
            params = [params]

        self.params = params or []
        self.client = client
        self.paths = []
        self.path_suites = []

    def __getattr__(self, param: str) -> "Executor":
        self.params.append(param)

        return self

    def __repr__(self) -> str:  # pragma: no cover
        return f'Executor(params={".".join(self.params)})'

    def __call__(self, **kwargs: Any) -> Any:
        return self.run(**kwargs)

    def install(self, paths: Union[AbstractSuiteInterface, Path, List[Path]]) -> None:
        # TODO only add suites & handle aliasing
        for p in paths:
            if isinstance(p, list):
                self.paths.extend(p)
            elif isinstance(p, Path):
                self.paths.append(p)
            else:  # AbstractSuiteInterface
                self.path_suites.append(p)

    def run(self, *, path: Optional[Path] = None, **kwargs: Any) -> Any:
        if not path:
            matching_paths = self.find_matching_path()

            if len(matching_paths) != 1:
                raise ClientError("Ambiguous call: matching paths # has to be 1")

            path = matching_paths[0]

        if not path.is_valid(self.client, **kwargs):
            raise ClientError("Invalid call!")

        api_path, query_args = path.get_path_and_qargs()
        response = self.client.http.request(
            api_path, method=path.method, query_args=query_args, data=kwargs.get("data")
        )  # TODO post data handling?

        return json_parser.parse_tree(response, path.response_structure)

    def find_matching_path(self) -> List[Path]:
        # TODO search in suites

        xxxxx = [p for p in self.paths if p.does_match(self.params)]
