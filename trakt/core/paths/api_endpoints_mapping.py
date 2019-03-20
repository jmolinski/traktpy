from __future__ import annotations

import re
from typing import Any, Dict
from typing import List as ListType
from typing import Union, cast

from trakt.core.models import Episode, Show
from trakt.core.paths.path import Path
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import PerArgValidator


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

    def get_countries(self, *, type: str, **kwargs: Any) -> ListType[Dict[str, str]]:
        ret = self.run("get_countries", type=type, **kwargs)
        return cast(ListType[Dict[str, str]], ret)


class CalendarsInterface(SuiteInterface):
    name = "calendars"

    paths = {
        "get_season_premieres": Path(
            "calendars/all/shows/premieres/?start_date/?days",
            [{"first_aired": str, "episode": Episode, "show": Show}],
            validators=[
                PerArgValidator("days", lambda t: isinstance(t, int)),
                PerArgValidator(
                    "start_date", lambda t: bool(re.match(r"\d{4}-\d{2}-\d{2}", t))
                ),
            ],
        )
    }

    def get_season_premieres(
        self, **kwargs: Any
    ) -> ListType[Dict[str, Union[str, Episode, Show]]]:
        ret = self.run("get_season_premieres", **kwargs)
        return ret
