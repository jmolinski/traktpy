from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from trakt.core.exceptions import ClientError
from trakt.core.paths.validators import (
    OptionalArgsValidator,
    RequiredArgsValidator,
    Validator,
)

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.abstract import AbstractApi

DEFAULT_VALIDATORS = [RequiredArgsValidator(), OptionalArgsValidator()]


class Path:
    path: str
    args: List[str]
    req_args: List[str]
    opt_args: List[str]
    methods: List[str]
    validators: List[Validator]
    aliases: List[str]

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
        allowed_filters: List[str] = None,
    ) -> None:
        self.path = path
        self._output_structure = output_structure

        if isinstance(methods, str):
            methods = [methods]

        self.methods = methods

        self.validators = DEFAULT_VALIDATORS + (validators or [])

        parts = path.split("/")
        default_alias = ".".join([p for p in parts if p[0] not in "?!"])
        args = [p for p in parts if p[0] in "?!"]
        self.req_args = [p for p in args if p[0] == "!"]
        self.opt_args = [p for p in args if p[0] == "?"]

        self.params = parts
        self.aliases = [default_alias] + (aliases or [])
        self.args = args

        self.qargs = qargs or []

        self.extended = extended or []
        self.filters = allowed_filters or []

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

        return "/".join(parts), qargs

    def is_bound(self) -> bool:
        return self.__bound_client is not None

    @property
    def response_structure(self) -> Any:
        return self._output_structure

    @property
    def method(self) -> str:
        return self.methods[0]
