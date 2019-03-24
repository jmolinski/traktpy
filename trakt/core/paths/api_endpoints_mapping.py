import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, cast

from trakt.core.models import Episode, Show
from trakt.core.paths.path import Path
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import COMMON_FILTERS, SHOWS_FILTERS, PerArgValidator


@dataclass
class SeasonPremiere:
    first_aired: str
    episode: Episode
    show: Show


class CountriesInterface(SuiteInterface):
    name = "countries"

    paths = {
        "get_countries": Path(
            "countries/!type",
            [{"name": str, "code": str}],
            aliases=["get_countries", ""],
            validators=[PerArgValidator("type", lambda t: t in {"shows", "movies"})],
        )
    }

    def get_countries(self, *, type: str, **kwargs: Any) -> List[Dict[str, str]]:
        ret = self.run("get_countries", type=type, **kwargs)
        return cast(List[Dict[str, str]], ret)


class CalendarsInterface(SuiteInterface):
    name = "calendars"

    paths = {
        "get_season_premieres": Path(
            "calendars/all/shows/premieres/?start_date/?days",
            [SeasonPremiere],
            validators=[
                PerArgValidator("days", lambda t: isinstance(t, int)),
                PerArgValidator(
                    "start_date", lambda t: re.match(r"\d{4}-\d{2}-\d{2}", t)
                ),
            ],
            filters=COMMON_FILTERS | SHOWS_FILTERS,
            extended=["full"],
        )
    }

    def get_season_premieres(self, **kwargs: Any) -> List[SeasonPremiere]:
        ret = self.run("get_season_premieres", **kwargs)
        return ret


class ShowsInterface(SuiteInterface):
    name = "shows"

    paths = {
        "get_trending": Path(
            "shows/trending",
            [{"watchers": int, "show": Show}],
            filters=COMMON_FILTERS | SHOWS_FILTERS,
            extended=["full"],
            pagination=True,
        )
    }

    def get_trending(self, **kwargs: Any) -> Iterable[Any]:
        ret = self.run("get_trending", **kwargs)
        return ret
