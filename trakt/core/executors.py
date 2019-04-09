from __future__ import annotations

import itertools
import time
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
    cast,
)

from trakt.core import json_parser
from trakt.core.exceptions import ArgumentError, ClientError

if TYPE_CHECKING:  # pragma: no cover
    from trakt.api import TraktApi
    from trakt.core.paths.suite_interface import SuiteInterface
    from trakt.core.paths.path import Path


class Executor:
    params: List[str]
    client: TraktApi
    paths: List[Path]
    path_suites: List[SuiteInterface]

    def __init__(
        self, client: TraktApi, params: Union[List[str], str, None] = None
    ) -> None:
        if isinstance(params, str):
            params = [params]

        self.params = params or []
        self.client = client
        self.paths = []
        self.path_suites = []

        if self.client.config["auto_refresh_token"] and self.client.user:
            expires_in = self.client.user.expires_at - int(time.time())

            if expires_in < self.client.config["oauth"]["refresh_token_s"]:
                self.client.oauth.refresh_token()

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
        return_code: bool = False,
        return_original: bool = False,
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
            return_code=return_code,
            return_original=return_original,
            **kwargs,
        )

        return_extras_enabled = pagination or return_code or return_original

        if return_extras_enabled:
            return [
                json_parser.parse_tree(response[0], path.response_structure),
                *response[1:],
            ]
        else:
            return json_parser.parse_tree(response, path.response_structure)

    def make_generator(self, path: Path, **kwargs: Any):
        start_page = int(kwargs.get("page", 1))
        per_page = int(kwargs.get("per_page", 10))
        max_pages = 1 << 16

        return PaginationIterator(self, path, start_page, per_page, max_pages)

    def find_matching_path(self) -> List[Path]:
        return [p for s in self.path_suites for p in s.find_matching(self.params)]


T = TypeVar("T")


class PaginationIterator(Iterable[T]):
    pages_total: Optional[int] = None

    def __init__(
        self,
        executor: Executor,
        path: Path,
        start_page: int,
        per_page: int,
        max_pages: int,
    ) -> None:
        self._executor = executor
        self._path = path
        self._start_page = start_page
        self._per_page = per_page
        self._max_pages = max_pages

        self._exhausted = False

    def __iter__(self) -> PaginationIterator[T]:
        if self._exhausted:
            return self

        self._exhausted = True
        self._page = self._start_page
        self._stop_at_page = self._max_pages

        self._queue: List[T] = []

        return self

    def __next__(self) -> T:
        if not self._queue:
            if not self._has_next_page():
                raise StopIteration()

            self._fetch_next_page()

        return self._queue.pop(0)

    def _fetch_next_page(self) -> None:
        response, pagination = self._executor.exec_path_call(
            self._path,
            pagination=True,
            extra_quargs={"page": str(self._page), "limit": str(self._per_page)},
        )

        for r in response:
            self._queue.append(r)

        self._page += 1
        self._stop_at_page = int(pagination["page_count"])
        self.pages_total = self._stop_at_page

    def prefetch_all(self) -> PaginationIterator[T]:
        iterator = cast(PaginationIterator[T], iter(self))
        while self._has_next_page():
            self._fetch_next_page()

        return iterator

    def _has_next_page(self) -> bool:
        return self._page <= self._stop_at_page

    def take(self, n: int) -> List[T]:
        if not isinstance(n, int) or n < 1:
            raise ArgumentError(
                f"argument n={n} is invalid; n must be an int and n >= 1"
            )

        it = iter(self)
        return list(itertools.islice(it, n))

    def take_all(self) -> List[T]:
        self.prefetch_all()
        return self.take(len(self._queue))

    def has_next(self) -> bool:
        return bool(self._queue or self._has_next_page())
