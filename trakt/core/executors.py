from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

from trakt.core import json_parser
from trakt.core.exceptions import ClientError

if TYPE_CHECKING:  # pragma: no cover
    from trakt.api import TraktApi
    from trakt.core.paths.suite_interface import SuiteInterface
    from trakt.core.paths.path import Path


class Executor:
    params: List[str]
    client: TraktApi
    path_suites: List[SuiteInterface]

    def __init__(self, client: TraktApi, params: Union[List[str], None] = None) -> None:
        self.params = params or []
        self.client = client
        self.path_suites = []

        if self.client.config["auto_refresh_token"] and self.client.user:
            expires_in = self.client.user.expires_at - int(time.time())

            if expires_in < self.client.config["oauth"]["refresh_token_s"]:
                self.client.oauth.refresh_token()

    def __repr__(self) -> str:  # pragma: no cover
        return f'Executor(params={".".join(self.params)})'

    def install(self, suites: List[SuiteInterface]) -> None:
        self.path_suites.extend(suites)

    def run(self, *, path: Optional[Path] = None, **kwargs: Any) -> Any:
        if not path:
            return self._delegate_to_interface(**kwargs)

        path.is_valid(self.client, **kwargs)  # raises

        if path.pagination:
            return self.make_generator(path, **kwargs)

        return self.exec_path_call(path, **kwargs)

    def _delegate_to_interface(self, **kwargs):
        matching_paths = self.find_matching_path()

        if len(matching_paths) != 1:
            raise ClientError("Invalid call: matching paths # has to be 1")

        path, interface_handler = matching_paths[0]

        return interface_handler(**kwargs)

    def exec_path_call(
        self,
        path: Path,
        extra_quargs: Optional[Dict[str, str]] = None,
        pagination: bool = False,
        return_code: bool = False,
        return_original: bool = False,
        **kwargs: Any,
    ):
        caching_enabled = self._should_use_cache(path, kwargs.get("no_cache", False))

        api_path, query_args = path.get_path_and_qargs()
        query_args.update(extra_quargs or {})

        api_response = self.client.http.request(
            api_path,
            method=path.method,
            query_args=query_args,
            data=kwargs.get("data"),
            use_cached=caching_enabled,
            **kwargs,
        )

        return_extras_enabled = pagination or return_code or return_original

        if return_extras_enabled:
            # TODO refactor
            result = [
                json_parser.parse_tree(api_response.json, path.response_structure)
            ]
            if return_code:
                result.append(api_response.original.status_code)
            if pagination:
                result.append(api_response.pagination)
            if return_original:
                result.append(api_response.original)

        else:
            result = json_parser.parse_tree(api_response.json, path.response_structure)

        if caching_enabled:
            # only runs if there were no errors
            self.client.http.cache_last_request()

        return result

    def _should_use_cache(self, path: Path, no_cache: bool):
        return no_cache is False and self.client.cache.accepted_level(path.cache_level)

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

                page += 1
                stop_at_page = int(pagination["page_count"]) + 1

        return generator()

    def find_matching_path(self) -> List[Tuple[Path, Callable]]:
        return [p for s in self.path_suites for p in s.find_matching(self.params)]


class CacheManager:
    client: TraktApi

    def __init__(self, client: TraktApi) -> None:
        self.client = client

    def accepted_level(self, level: str) -> bool:
        max_allowed = self.client.config["cache"]["cache_level"]

        if level == "no":
            return False
        elif level == "basic":
            return max_allowed in {"basic", "full"}
        elif level == "full":
            return max_allowed == "full"
        else:
            raise ClientError("invalid cache level")

    def get(self, *args, **kwargs) -> Any:
        pass

    def set(self, x) -> None:
        pass

    def has(self, *args, **kwargs) -> bool:
        return False
