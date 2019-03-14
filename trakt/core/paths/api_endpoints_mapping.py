from typing import Any, Dict, cast

from trakt.core.abstract import AbstractApi, AbstractSuiteInterface

# from trakt.core.executors import Executor
from trakt.core.models import *
from trakt.core.paths.path import Path
from trakt.core.paths.validators import PerArgValidator

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


PATHS = []


class SuiteInterface(AbstractSuiteInterface):
    paths: Dict[str, Path]
    client: AbstractApi

    def __init__(self, client: AbstractApi) -> None:
        self.client = client
        self.paths = {}

    def find_match(self, name: str) -> None:
        return self.paths.get(name)

    def run(self, command: str, **kwargs: Any) -> Any:
        return Executor(self.client).run(path=self.paths[command], **kwargs)


class CountriesInterface(SuiteInterface):
    paths = {
        "get_countries": Path(
            "countries/!type",
            [{"name": str, "code": str}],
            aliases=["get_countries"],
            validators=[PerArgValidator("type", lambda t: t in {"shows", "movies"})],
        )
    }

    def get_countries(self, *, type: str, **kwargs: Any) -> Dict[str, str]:
        ret = self.run("get_countries", type=type, **kwargs)
        return cast(ret, Dict[str, str])
