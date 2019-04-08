from typing import Iterable, List, Optional, Union

from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import SearchResult
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import ALL_FILTERS, PerArgValidator

MEDIA_TYPES = ["movie", "show", "episode", "person", "list"]
ID_TYPES = ["trakt", "imdb", "tmdb", "tvdb"]
POSSIBLE_FIELDS = {
    "title",
    "tagline",
    "overview",
    "people",
    "translations",
    "aliases",
    "name",
    "biography",
    "description",
}


class SearchI(SuiteInterface):
    name = "search"

    paths = {
        "text_query": Path(  # type: ignore
            "search/!type",
            [SearchResult],
            extended=["full"],
            filters=ALL_FILTERS,
            pagination=True,
            validators=[
                PerArgValidator(
                    "type", lambda t: all(x in MEDIA_TYPES for x in t.split(","))
                ),
                PerArgValidator("query", lambda q: isinstance(q, str) and q),
                PerArgValidator(
                    "fields", lambda f: all(x in POSSIBLE_FIELDS for x in f.split(","))
                ),
            ],
            qargs=["fields"],
        ),
        "id_lookup": Path(  # type: ignore
            "search/!id_type/!id",
            [SearchResult],
            extended=["full"],
            filters=ALL_FILTERS,
            pagination=True,
            validators=[
                PerArgValidator("id", lambda t: isinstance(t, (int, str))),
                PerArgValidator("id_type", lambda it: it in ID_TYPES),
                PerArgValidator(
                    "type", lambda f: all(x in MEDIA_TYPES for x in f.split(","))
                ),
            ],
            qargs=["type"],
        ),
    }

    def text_query(
        self,
        type: Union[str, List[str]],
        query: str,
        fields: Optional[Union[str, List[str]]] = None,
        **kwargs
    ) -> Iterable[SearchResult]:
        type = [type] if isinstance(type, str) else type
        type = ",".join(type)
        req = {"type": type, "query": query}

        if fields:
            fields = [fields] if isinstance(fields, str) else fields
            req["fields"] = ",".join(fields)

        return self.run("text_query", **kwargs, **req)

    def id_lookup(
        self,
        id_type: str,
        id: Union[str, int],
        type: Optional[Union[str, List[str]]] = None,
        **kwargs
    ) -> Iterable[SearchResult]:
        req = {"id_type": id_type, "id": id}

        if type:
            type = [type] if isinstance(type, str) else type
            req["type"] = ",".join(type)

        return self.run("id_lookup", **kwargs, **req)
