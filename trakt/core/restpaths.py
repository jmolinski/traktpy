from typing import Any, Dict, List

from trakt.core.abstract import AbstractApi
from trakt.core.exceptions import ClientError


class Validator:
    def _validate(self, *args, **kwargs):
        return True

    def validate(self, *args, **kwargs):
        return self._validate(*args, **kwargs) is not False


class AuthRequiredValidator(Validator):
    def _validate(self, client, *args, **kwargs):
        if not client.authenticated:
            return False


class RequiredArgsValidator(Validator):
    def _validate(self, *args, path=None, **kwargs):
        for p in path.req_args:
            arg_name = p[1:]
            if arg_name not in kwargs or kwargs[arg_name] in (None, [], {}):
                return False


class OptionalArgsValidator(Validator):
    ...


class Path:
    path: str
    args: List[str]
    req_args: List[str]
    opt_args: List[str]
    methods: List[str]
    validators: List[Validator]
    aliases: List[str]

    _output_structure: Any

    __bound_client: AbstractApi
    __bound_args: List[Any]
    __bound_kwargs: Dict[str, Any]

    def __init__(
        self, path, output_structure, methods="GET", validators=None, qargs=None
    ):
        self.path = path
        self._output_structure = output_structure

        if isinstance(methods, str):
            methods = [methods]

        self.methods = methods

        self.validators = [RequiredArgsValidator(), OptionalArgsValidator()] + (
            validators or []
        )

        parts = path.split("/")
        default_alias = [p for p in parts if p[0] not in "?!"]
        args = [p for p in parts if p[0] in "?!"]
        self.req_args = [p for p in args if p[0] == "!"]
        self.opt_args = [p for p in args if p[0] == "?"]

        self.params = parts
        self.aliases = [default_alias]
        self.args = args

        self.qargs = qargs or []

        self.__bound_client = None

    def does_match(self, params):
        return any(alias == params for alias in self.aliases)

    def is_valid(self, client, *args, **kwargs):
        validation_result = all(
            v.validate(self, client=client, path=self, *args, **kwargs)
            for v in self.validators
        )

        if validation_result:
            self.__bound_client = client
            self.__bound_args = args
            self.__bound_kwargs = kwargs

        return validation_result

    def _get_param_value(self, param):
        if param not in self.args:
            return param

        arg_name = param[1:]

        if param in self.req_args:
            return self.__bound_kwargs[arg_name]

        if param in self.opt_args:
            return self.__bound_kwargs.get(arg_name)

    def get_path_and_qargs(self):
        if not self.is_bound():
            raise ClientError("call .is_valid first!")

        parts = [self._get_param_value(p) for p in self.params]
        parts = [str(p) for p in parts if p]  # omit None (empty optional params)

        qargs = {
            q: self.__bound_kwargs[q] for q in self.qargs if q in self.__bound_kwargs
        }

        return "/".join(parts), qargs

    def is_bound(self):
        return self.__bound_client is not None

    @property
    def response_structure(self):
        return self._output_structure

    @property
    def method(self):
        return self.methods[0]


REQ_AUTH = [AuthRequiredValidator()]

"""
OAUTH = [("oath/device/code", "GET"), ("oath/device/token", "POST")]

cal_validators = []
CALENDARS = [
    ("calendars/my/shows/?start_date/?days", "GET", cal_validators + REQ_AUTH),
    ("calendars/my/shows/new/?start_date/?days", "GET", cal_validators + REQ_AUTH),
    (
        "calendars/my/shows/premieres/?start_date/?days",
        "GET",
        cal_validators + REQ_AUTH,
    ),
    ("calendars/my/movies/?start_date/?days", "GET", cal_validators + REQ_AUTH),
    ("calendars/my/dvd/?start_date/?days", "GET", cal_validators + REQ_AUTH),
    ("calendars/all/shows/?start_date/?days", "GET", cal_validators),
    ("calendars/all/shows/new/?start_date/?days", "GET", cal_validators),
    ("calendars/all/shows/premieres/?start_date/?days", "GET", cal_validators),
    ("calendars/all/movies/?start_date/?days", "GET", cal_validators),
    ("calendars/all/dvd/?start_date/?days", "GET", cal_validators),
]

PATHS = OAUTH + CALENDARS
"""

COUNTRIES = [Path("countries/!type", [{"name": str, "code": str}])]

PATHS = COUNTRIES
