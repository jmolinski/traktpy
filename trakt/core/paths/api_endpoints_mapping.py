from trakt.core.paths.path import Path

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
