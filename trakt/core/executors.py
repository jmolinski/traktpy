from typing import List, Union

from trakt.core import json_parser
from trakt.core.abstract import AbstractApi
from trakt.core.exceptions import ClientError
from trakt.core.paths.path import Path


class Executor:
    params: List[str]
    client: AbstractApi
    paths: List[Path]

    def __init__(self, client: AbstractApi, params: Union[List[str], str]) -> None:
        if isinstance(params, str):
            params = [params]

        self.params = params
        self.client = client
        self.paths = []

    def __getattr__(self, param: str) -> "Executor":
        self.params.append(param)

        return self

    def __repr__(self) -> str:  # pragma: no cover
        return f'Executor(params={".".join(self.params)})'

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def install(self, paths):
        if isinstance(paths, list):
            self.paths.extend(paths)
        else:
            self.paths.append(paths)

    def run(self, *args, **kwargs):
        matching_paths = self.find_matching_path()

        if len(matching_paths) != 1:
            raise ClientError("Ambiguous call: matching paths # has to be 1")

        path = matching_paths[0]

        if not path.is_valid(self.client, *args, **kwargs):
            raise ClientError("Invalid call!")

        api_path, query_args = path.get_path_and_qargs()
        response = self.client.http.request(
            api_path, method=path.method, query_args=query_args, data=kwargs.get("data")
        )  # TODO post data handling?

        return json_parser.parse_tree(response, path.response_structure)

    def find_matching_path(self):
        return [p for p in self.paths if p.does_match(self.params)]
