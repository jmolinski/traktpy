from typing import List, Union

from trakt.core.models import Movie
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import Show
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import AuthRequiredValidator, PerArgValidator

IGNORE_COLLECTED_VALIDATOR = PerArgValidator(
    "ignore_collected", lambda i: isinstance(i, bool)
)
ID_VALIDATOR = PerArgValidator("id", lambda c: isinstance(c, (int, str)))


class RecommendationsI(SuiteInterface):
    name = "recommendations"

    paths = {
        "get_movie_recommendations": Path(
            "recommendations/movies",
            [Movie],
            validators=[AuthRequiredValidator(), IGNORE_COLLECTED_VALIDATOR],
            extended=["full"],
        ),
        "hide_movie": Path(
            "recommendations/movies/!id",
            {},
            validators=[AuthRequiredValidator(), ID_VALIDATOR],
        ),
        "get_show_recommendations": Path(
            "recommendations/shows",
            [Show],
            validators=[AuthRequiredValidator(), IGNORE_COLLECTED_VALIDATOR],
            extended=["full"],
        ),
        "hide_show": Path(
            "recommendations/shows/!id",
            {},
            validators=[AuthRequiredValidator(), ID_VALIDATOR],
        ),
    }

    def get_movie_recommendations(
        self, *, ignore_collected: bool = False, **kwargs
    ) -> List[Movie]:
        return self.run(
            "get_movie_recommendations", **kwargs, ignore_collected=ignore_collected
        )

    def hide_movie(self, *, movie: Union[Movie, str, int], **kwargs) -> None:
        id = self._generic_get_id(movie)
        self.run("hide_movie", **kwargs, id=id)

    def get_show_recommendations(
        self, *, ignore_collected: bool = False, **kwargs
    ) -> List[Show]:
        return self.run(
            "get_show_recommendations", **kwargs, ignore_collected=ignore_collected
        )

    def hide_show(self, *, show: Union[Movie, str, int], **kwargs) -> None:
        id = self._generic_get_id(show)
        self.run("hide_show", **kwargs, id=id)
