from typing import List, Union

from trakt.core.models import Person, TraktList
from trakt.core.paths.endpoint_mappings.movies import LIST_SORT_VALUES, LIST_TYPE_VALUES
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import MovieCredits, ShowCredits
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import PerArgValidator

PERSON_ID_VALIDATOR = PerArgValidator("id", lambda c: isinstance(c, (int, str)))


class PeopleI(SuiteInterface):
    name = "people"

    paths = {
        "get_person": Path(
            "people/!id",
            Person,
            validators=[PERSON_ID_VALIDATOR],
            extended=["full"],
            cache_level="basic",
        ),
        "get_movie_credits": Path(
            "people/!id/movies",
            MovieCredits,
            validators=[PERSON_ID_VALIDATOR],
            extended=["full"],
            cache_level="basic",
        ),
        "get_show_credits": Path(
            "people/!id/shows",
            ShowCredits,
            validators=[PERSON_ID_VALIDATOR],
            extended=["full"],
            cache_level="basic",
        ),
        "get_lists": Path(
            "people/!id/lists/?type/?sort",
            [TraktList],
            validators=[
                PERSON_ID_VALIDATOR,
                PerArgValidator("type", lambda t: t in LIST_TYPE_VALUES),
                PerArgValidator("sort", lambda s: s in LIST_SORT_VALUES),
            ],
            extended=["full"],
            cache_level="basic",
        ),
    }

    def get_person(self, person: Union[Person, str, int], **kwargs) -> Person:
        id = self._get_person_id(person)
        return self.run("get_person", **kwargs, id=id)

    def get_movie_credits(
        self, person: Union[Person, str, int], **kwargs
    ) -> MovieCredits:
        id = self._get_person_id(person)
        return self.run("get_movie_credits", **kwargs, id=id)

    def get_show_credits(
        self, person: Union[Person, str, int], **kwargs
    ) -> ShowCredits:
        id = self._get_person_id(person)
        return self.run("get_show_credits", **kwargs, id=id)

    def get_lists(self, person: Union[Person, str, int], **kwargs) -> List[TraktList]:
        id = self._get_person_id(person)
        return self.run("get_lists", **kwargs, id=id)

    def _get_person_id(self, p: Union[Person, int, str]) -> str:
        return str(self._generic_get_id(item=p))
