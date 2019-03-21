from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from trakt.core import json_parser
from trakt.core.exceptions import ClientError

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.abstract import AbstractApi
    from trakt.core.paths.suite_interface import SuiteInterface
    from trakt.core.paths.path import Path


class Executor:
    params: List[str]
    client: AbstractApi
    paths: List[Path]
    path_suites: List[SuiteInterface]

    def __init__(
        self, client: AbstractApi, params: Union[List[str], str, None] = None
    ) -> None:
        if isinstance(params, str):
            params = [params]

        self.params = params or []
        self.client = client
        self.paths = []
        self.path_suites = []

        if self.client.config["auto_refresh_token"] and self.client.user:
            self.client.oauth.refresh_token()

    def __getattr__(self, param: str) -> Executor:
        self.params.append(param)
        return self

    def __repr__(self) -> str:  # pragma: no cover
        return f'Executor(params={".".join(self.params)})'

    def __call__(self, **kwargs: Any) -> Any:
        return self.run(**kwargs)

    def install(self, suites: List[SuiteInterface]) -> None:
        self.path_suites.extend(suites)

    def run(self, *, path: Optional[Path] = None, **kwargs: Any) -> Any:
        if not path:
            matching_paths = self.find_matching_path()

            if len(matching_paths) != 1:
                raise ClientError("Ambiguous call: matching paths # has to be 1")

            path = matching_paths[0]

        if not path.is_valid(self.client, **kwargs):
            raise ClientError("Invalid call!")

        if path.pagination:
            return self.make_generator(path, **kwargs)

        return self.exec_path_call(path, **kwargs)

    def exec_path_call(
        self,
        path: Path,
        extra_quargs: Optional[Dict[str, str]] = None,
        pagination: bool = False,
        **kwargs: Any,
    ):
        api_path, query_args = path.get_path_and_qargs()
        query_args.update(extra_quargs or {})

        response = self.client.http.request(
            api_path,
            method=path.method,
            query_args=query_args,
            data=kwargs.get("data"),
            return_pagination=pagination,
        )

        if pagination:
            (json_response, *r) = response
            return (json_parser.parse_tree(json_response, path.response_structure), *r)

        return json_parser.parse_tree(response, path.response_structure)

    def make_generator(self, path: Path, **kwargs: Any):
        start_page = int(kwargs.get("page", 1))
        per_page = int(kwargs.get("per_page", 10))
        max_pages = 10e10

        def generator():
            page = start_page
            stop_at_page = max_pages

            while page < stop_at_page:
                response, pagination = self.exec_path_call(
                    path,
                    pagination=True,
                    extra_quargs={"page": str(page), "limit": str(per_page)},
                )

                yield from response

                stop_at_page = int(pagination["page_count"]) + 1
                page += 1

        return generator()

    def find_matching_path(self) -> List[Path]:
        return [p for s in self.path_suites for p in s.find_matching(self.params)]
