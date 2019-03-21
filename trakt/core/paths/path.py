from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Union

from trakt.core.exceptions import ClientError
from trakt.core.paths.validators import (
    MULTI_FILTERS,
    ExtendedValidator,
    FiltersValidator,
    OptionalArgsValidator,
    RequiredArgsValidator,
    Validator,
)

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.abstract import AbstractApi

DEFAULT_VALIDATORS = [
    RequiredArgsValidator(),
    OptionalArgsValidator(),
    ExtendedValidator(),
    FiltersValidator(),
]


class Path:
    path: str
    args: List[str]
    req_args: List[str]
    opt_args: List[str]
    methods: List[str]
    validators: List[Validator]
    aliases: List[str]
    extended: List[str]
    filters: Set[str]
    pagination: bool

    _output_structure: Any

    __bound_client: Optional[AbstractApi]
    __bound_kwargs: Dict[str, Any]

    def __init__(
        self,
        path: str,
        output_structure: Any,
        methods: Union[str, List[str]] = "GET",
        validators: List[Validator] = None,
        qargs: Dict[str, str] = None,
        aliases: List[str] = None,
        extended: List[str] = None,
        filters: Set[str] = None,
        pagination: bool = False,
    ) -> None:
        self.path = path
        self._output_structure = output_structure

        if isinstance(methods, str):
            methods = [methods]

        self.methods = methods
        self.validators = DEFAULT_VALIDATORS + (validators or [])

        self.params = path.split("/")
        self.args = [p for p in self.params if p[0] in "?!"]
        self.req_args = [p for p in self.args if p[0] == "!"]
        self.opt_args = [p for p in self.args if p[0] == "?"]

        default_alias = ".".join([p for p in self.params if p[0] not in "?!"])
        self.aliases = [default_alias] + (aliases or [])

        self.qargs = qargs or []

        self.extended = extended or []
        self.filters = filters or set()

        self.pagination = pagination

        self.__bound_client = None

    def does_match(self, name: str) -> bool:
        return name in self.aliases

    def is_valid(self, client: AbstractApi, **kwargs: Any) -> bool:
        for v in self.validators:
            v.validate(self, client=client, path=self, **kwargs)  # may raise

        self.__bound_client = client
        self.__bound_kwargs = kwargs

        return True

    def _get_param_value(self, param: str) -> Any:
        if param not in self.args:
            return param

        arg_name = param[1:]

        if param in self.req_args:
            return self.__bound_kwargs[arg_name]

        if param in self.opt_args:
            return self.__bound_kwargs.get(arg_name)

    def get_path_and_qargs(self) -> Tuple[str, Dict[str, Any]]:
        if not self.is_bound():
            raise ClientError("call .is_valid first!")

        parts = [self._get_param_value(p) for p in self.params]
        parts = [str(p) for p in parts if p]  # omit None (empty optional params)

        qargs = {
            q: self.__bound_kwargs[q] for q in self.qargs if q in self.__bound_kwargs
        }

        qargs.update(self._get_parsed_filters())

        if "extended" in self.__bound_kwargs and self.__bound_kwargs["extended"]:
            if self.__bound_kwargs["extended"] is True:
                # if len(self.extended) == 1 setting extended=True
                # sets it to the proper val (meta or full)
                self.__bound_kwargs["extended"] = self.extended[0]

            qargs["extended"] = self.__bound_kwargs["extended"]

        return "/".join(parts), qargs

    def _get_parsed_filters(self) -> Dict[str, str]:
        m = {}

        for f in self.filters:
            if f in self.__bound_kwargs:
                val = self.__bound_kwargs[f]

                if f in MULTI_FILTERS and isinstance(val, (tuple, list)):
                    val = ",".join(val)

                m[f] = str(val)

        return m

    def is_bound(self) -> bool:
        return self.__bound_client is not None

    @property
    def response_structure(self) -> Any:
        return self._output_structure

    @property
    def method(self) -> str:
        return self.methods[0]
