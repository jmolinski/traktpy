from typing import List


class Validator:
    def _validate(self, *args, **kwargs):
        return True

    def validate(self, *args, **kwargs):  # TODO should raise?
        return self._validate(*args, **kwargs) is not False


class AuthRequiredValidator(Validator):
    def _validate(self, client, *args, **kwargs):
        if not client.authenticated:
            return False


class Path:
    path: str
    args: List[str]
    methods: List[str]
    validators: List[Validator]
    aliases: List[str]

    def __init__(self, path, methods="GET", validators=None):
        self.path = path

        if isinstance(methods, str):
            methods = [methods]

        self.methods = methods

        if not validators:
            validators = list()

        self.validators = validators

        parts = path.split()
        default_alias = [p for p in parts if p[0] not in "?!"]
        args = [p for p in parts if p[0] in "?!"]

        self.params = parts
        self.aliases = [default_alias]
        self.args = args

    def does_match(self, params):
        return any(alias == params for alias in self.aliases)

    def is_valid(self, *args, **kwargs):
        return all(v.validate(self, *args, **kwargs) for v in self.validators)

    def get_path(self):
        return "/".join(self.params)  # TODO supply args


REQ_AUTH = [AuthRequiredValidator()]

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
