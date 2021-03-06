from dataclasses import dataclass
from datetime import datetime
from typing import Any

import pytest
from tests.test_data.episodes import EPISODE, EXTENDED_EPISODE
from tests.test_data.lists import LIST, TRENDING_LISTS, USER
from tests.test_data.shows import EXTENDED_SHOW, SHOW
from trakt.core import json_parser
from trakt.core.exceptions import TraktResponseError
from trakt.core.models import Episode, Show, TraktList, User
from trakt.core.paths.response_structs import ListResponse


@dataclass
class MockClassName:
    name: str


@dataclass
class MockClassDateData:
    date: int
    data: MockClassName


def test_basic_list_dict():
    data = ["abc", "xyz"]
    tree_struct = [str]

    parsed = json_parser.parse_tree(data, tree_struct)

    assert parsed == ["abc", "xyz"]

    data = {"name": "Poland", "code": "pl"}
    tree_struct = {"name": str, "code": str}

    parsed = json_parser.parse_tree(data, tree_struct)

    assert parsed == data


def test_dataclass():
    data = {"name": "xyz"}
    tree_struct = MockClassName

    parsed = json_parser.parse_tree(data, tree_struct)

    assert parsed.__class__ == MockClassName
    assert parsed.name == "xyz"

    data = [{"name": "xyz"}, {"name": "abc"}]
    tree_struct = [MockClassName]

    parsed = json_parser.parse_tree(data, tree_struct)

    assert parsed.__class__ == list
    assert parsed[1].__class__ == MockClassName
    assert parsed[1].name == "abc"


def test_mixed_structure():
    data = {
        "count": 2,
        "items": [
            {"info": "m-1", "obj": {"date": 2018, "data": {"name": "xxi"}}},
            {"info": "m-2", "obj": {"date": 1410, "data": {"name": "xv"}}},
        ],
    }
    tree_struct = {"count": int, "items": [{"info": str, "obj": MockClassDateData}]}

    parsed = json_parser.parse_tree(data, tree_struct)

    assert parsed.__class__ == dict
    assert "count" in parsed and parsed["count"].__class__ == int
    assert "items" in parsed and parsed["items"][0].__class__ == dict

    item = parsed["items"][1]

    assert "info" in item and item["info"] == "m-2"
    assert "obj" in item and item["obj"].__class__ == MockClassDateData
    assert item["obj"].data.__class__ == MockClassName


def test_defaults():
    data = {"a": "b"}
    tree_struct = {"a": "c", "d": "e"}

    parsed = json_parser.parse_tree(data, tree_struct)

    assert parsed["a"] == "b"
    assert parsed["d"] == "e"
    assert json_parser.parse_tree(data, {}) == {}


def test_wildcards():
    data = {"a": 100, "c": "d", "e": "f", True: "g", 0.5: "y", 0.7: 10}
    tree_struct = {"a": int, str: str, float: Any}

    parsed = json_parser.parse_tree(data, tree_struct)

    assert parsed["a"] == 100
    assert parsed["c"] == "d"
    assert parsed["e"] == "f"
    assert True not in parsed
    assert parsed[0.5] == "y"
    assert parsed[0.7] == 10


def test_parser_nofail():
    ep = json_parser.parse_tree(EPISODE, Episode)
    epex = json_parser.parse_tree(EXTENDED_EPISODE, Episode)

    sh = json_parser.parse_tree(SHOW, Show)
    shex = json_parser.parse_tree(EXTENDED_SHOW, Show)

    l = json_parser.parse_tree(LIST, TraktList)
    tl = json_parser.parse_tree(TRENDING_LISTS, [ListResponse])

    u = json_parser.parse_tree(USER, User)


def test_parser_datetime():
    show = json_parser.parse_tree(EXTENDED_SHOW, Show)

    assert isinstance(show.first_aired, datetime)
    assert show.first_aired == datetime.strptime(
        EXTENDED_SHOW["first_aired"][:-5] + "Z", "%Y-%m-%dT%H:%M:%S%z"
    )


def test_parser_default_none():
    show = json_parser.parse_tree(EXTENDED_SHOW, Show)

    assert show.country == "gb"
    assert show.trailer is None


def test_parser_invalid_structure():
    with pytest.raises(TraktResponseError):
        json_parser.parse_tree([{"a": "b"}], Show)


def test_empty_resp():
    data_list = json_parser.parse_tree([], [])
    data_dict = json_parser.parse_tree({}, {})

    assert data_dict == {}
    assert data_list == []
