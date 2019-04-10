from __future__ import annotations

import itertools
import time
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from trakt.core import json_parser
from trakt.core.components.cache import FrozenRequest
from trakt.core.exceptions import ArgumentError, ClientError

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
            return self._make_generator(path, **kwargs)

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
        return_extras: bool = False,
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

        api_response.parsed = json_parser.parse_tree(
            api_response.json, path.response_structure
        )

        if caching_enabled:
            # only runs if there were no errors
            last_request = cast(FrozenRequest, self.client.http.last_request)
            self.client.cache.set(last_request)

        return api_response if return_extras else api_response.parsed

    def _should_use_cache(self, path: Path, no_cache: bool):
        return no_cache is False and self.client.cache.accepted_level(path.cache_level)

    def _make_generator(self, path: Path, **kwargs: Any):
        start_page = int(kwargs.get("page", 1))
        per_page = int(kwargs.get("per_page", 10))
        max_pages = 1 << 16

        return PaginationIterator(self, path, start_page, per_page, max_pages)

    def find_matching_path(self) -> List[Tuple[Path, Callable]]:
        return [p for s in self.path_suites for p in s.find_matching(self.params)]


T = TypeVar("T")
PER_PAGE_LIMIT = 100


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
        self._queue: List[T] = []
        self._yielded_items = 0

    def __iter__(self) -> PaginationIterator[T]:
        if self._exhausted:
            return self

        self._exhausted = True
        self._page = self._start_page
        self._stop_at_page = self._max_pages

        self._queue = []
        self._yielded_items = 0

        return self

    def __next__(self) -> T:
        if not self._queue:
            if not self._has_next_page():
                raise StopIteration()

            self._fetch_next_page()

        self._yielded_items += 1
        return self._queue.pop(0)

    def _fetch_next_page(self, skip_first: int = 0) -> None:
        response = self._executor.exec_path_call(
            self._path,
            return_extras=True,
            extra_quargs={"page": str(self._page), "limit": str(self._per_page)},
        )

        for r in response.parsed[skip_first:]:
            self._queue.append(r)

        self._page += 1
        self._stop_at_page = int(response.pagination["page_count"])
        self.pages_total = self._stop_at_page

    def prefetch_all(self) -> PaginationIterator[T]:
        """Prefetch all results. Optimized."""
        iterator = cast(PaginationIterator[T], iter(self))

        if not self._has_next_page():
            return iterator

        # tweak per_page setting to make fetching as fast as possible
        old_per_page = self._per_page
        self._per_page = PER_PAGE_LIMIT

        self._page = (self._yielded_items // PER_PAGE_LIMIT) + 1
        to_skip = (self._yielded_items % PER_PAGE_LIMIT) + len(self._queue)

        self._fetch_next_page(skip_first=to_skip)

        while self._has_next_page():
            self._fetch_next_page()

        self._per_page = old_per_page

        return iterator

    def _has_next_page(self) -> bool:
        return self._page <= self._stop_at_page

    def take(self, n: int = -1) -> List[T]:
        """Take n next results. By default returns per_page results."""
        if n == -1:
            n = self._per_page

        if not isinstance(n, int) or n < 0:
            raise ArgumentError(
                f"argument n={n} is invalid; n must be an int and n >= 1"
            )

        it = iter(self)
        return list(itertools.islice(it, n))

    def take_all(self) -> List[T]:
        """Take all available results."""
        self.prefetch_all()
        return self.take(len(self._queue))

    def has_next(self) -> bool:
        """Check if there are any results left."""
        if not self._exhausted:
            iter(self)

        return bool(self._queue or self._has_next_page())
