import pytest
from tests.test_data.lists import LIST
from tests.test_data.people import MOVIE_CREDITS, PERSON, SHOW_CREDITS
from tests.utils import mk_mock_client
from trakt.core.exceptions import ArgumentError
from trakt.core.json_parser import parse_tree
from trakt.core.models import Person


def test_get_person():
    client = mk_mock_client({r".*people.*": [PERSON, 200]})
    person = parse_tree(PERSON, Person)

    with pytest.raises(ArgumentError):
        client.people.get_person(person=0.5)

    assert client.people.get_person(person=person.ids["trakt"]).name == PERSON["name"]
    assert client.people.get_person(person=person).name == PERSON["name"]


def test_get_movie_credits():
    client = mk_mock_client({r".*people.*": [MOVIE_CREDITS, 200]})

    credits = client.people.get_movie_credits(person=123)
    assert credits.cast[0].character == MOVIE_CREDITS["cast"][0]["character"]


def test_get_show_credits():
    client = mk_mock_client({r".*people.*": [SHOW_CREDITS, 200]})

    credits = client.people.get_show_credits(person=123)
    expected = SHOW_CREDITS["crew"]["production"][0]["job"]
    assert credits.crew.production[0].job == expected


def test_get_lists():
    client = mk_mock_client({r".*people.*": [[LIST], 200]})

    lists = list(client.people.get_lists(person=123))

    assert len(lists) == 1
    assert lists[0].name == LIST["name"]
