# (path, method, validators,)


class Validator:
    def validate(self, *args, **kwargs):
        return True


class AuthRequiredValidator(Validator):
    def validate(self, client, *args, **kwargs):
        if not client.authenticated:
            return False  # TODO should raise?


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


def resolve_path(params):
    pass
