from typing import Any, Dict, List, Tuple, Union

from trakt.core.abstract import AbstractApi
from trakt.core.exceptions import ClientError
from trakt.core.paths.validators import (
    OptionalArgsValidator,
    RequiredArgsValidator,
    Validator,
)

DEFAULT_VALIDATORS = [RequiredArgsValidator(), OptionalArgsValidator()]


class Path:
    path: str
    args: List[str]
    req_args: List[str]
    opt_args: List[str]
    methods: List[str]
    validators: List[Validator]
    aliases: List[List[str]]

    _output_structure: Any

    __bound_client: AbstractApi
    __bound_kwargs: Dict[str, Any]

    def __init__(
        self,
        path: str,
        output_structure: Any,
        methods: Union[str, List[str]] = "GET",
        validators: List[Validator] = None,
        qargs: Dict[str, str] = None,
        aliases: List[str] = None,
    ) -> None:
        self.path = path
        self._output_structure = output_structure

        if isinstance(methods, str):
            methods = [methods]

        self.methods = methods

        self.validators = DEFAULT_VALIDATORS + (validators or [])

        parts = path.split("/")
        default_alias = [p for p in parts if p[0] not in "?!"]
        args = [p for p in parts if p[0] in "?!"]
        self.req_args = [p for p in args if p[0] == "!"]
        self.opt_args = [p for p in args if p[0] == "?"]

        self.params = parts
        aliases = aliases or []
        split_aliases = [a.split(".") for a in aliases]
        self.aliases = [default_alias] + split_aliases
        self.args = args

        self.qargs = qargs or []

        self.__bound_client = None

    def does_match(self, params: List[str]) -> bool:
        return any(alias == params for alias in self.aliases)

    def is_valid(self, client: AbstractApi, **kwargs: Any) -> bool:
        validation_result = all(
            v.validate(self, client=client, path=self, **kwargs)
            for v in self.validators
        )

        if validation_result:
            self.__bound_client = client
            self.__bound_kwargs = kwargs

        return validation_result

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
