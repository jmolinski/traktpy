from __future__ import annotations

from typing import Any, Dict, cast

from trakt.core.models import Movie
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

    def get_countries(self, *, type: str, **kwargs: Any) -> Dict[str, str]:
        ret = self.run("get_countries", type=type, **kwargs)
        return cast(Dict[str, str], ret)
