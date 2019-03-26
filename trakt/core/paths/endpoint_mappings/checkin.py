from typing import Any, Dict, Union

from trakt.core.decorators import auth_required
from trakt.core.models import Movie, Episode
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.path import Path


class CheckinI(SuiteInterface):
    name = "checkin"

    paths = {Path("checkin", {}, methods="DELETE")}

    @auth_required
    def check_into(
        self,
        *,
        movie: Union[Movie, Dict[str, Any]] = None,
        episode: Episode = None,
        **kwargs: Any
    ) -> int:
        return self.run("get_trending", **kwargs)

    @auth_required
    def delete_active_checking(self, **kwargs: Any) -> None:
        self.run("checkin", **kwargs)
