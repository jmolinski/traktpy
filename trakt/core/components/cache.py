from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:  # pragma: no cover
    from trakt.api import TraktApi


class CacheLevel(Enum):
    NO = "no"
    BASIC = "basic"
    FULL = "full"


class CacheManager:
    client: TraktApi
    _cache: Dict[FrozenRequest, datetime]

    CACHE_LEVELS = (CacheLevel.NO, CacheLevel.BASIC, CacheLevel.FULL)

    def __init__(self, client: TraktApi) -> None:
        self.client = client
        self._cache = {}

    def accepted_level(self, level: CacheLevel) -> bool:
        max_allowed = CacheLevel(self.client.config["cache"]["cache_level"])

        if level == CacheLevel.NO:
            return False
        elif level == CacheLevel.BASIC:
            return max_allowed in {CacheLevel.BASIC, CacheLevel.FULL}
        else:  # "full"
            return max_allowed == CacheLevel.FULL

    def get(self, wanted: FrozenRequest) -> FrozenRequest:
        if not self.has(wanted):
            raise LookupError("Request not in cache")

        return [r for r in self._cache.keys() if r == wanted][0]

    def set(self, req: FrozenRequest) -> None:
        cache_timeout = self.client.config["cache"]["timeout"]
        valid_till = datetime.now() + timedelta(seconds=cache_timeout)
        self._cache[req] = valid_till

    def has(self, req: FrozenRequest) -> bool:
        if req not in self._cache:
            return False

        valid_till = self._cache[req]
        if datetime.now() > valid_till:
            del self._cache[req]
            return False

        return True


class FrozenRequest:
    def __init__(
        self,
        path: str,
        query_args: Dict[str, str],
        headers: Dict[str, str],
        response: Any = None,
    ) -> None:
        self.path = path
        self.query_args = query_args
        self.headers = headers
        self.response = response

    @property
    def _unique_id(self) -> str:
        qargs_repr = repr(sorted(self.query_args.items()))
        headers_repr = repr(sorted(self.headers.items()))
        return self.path + qargs_repr + headers_repr

    def __hash__(self):
        return hash(self._unique_id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FrozenRequest):
            return self._unique_id == other._unique_id
        return False  # pragma: no cover
