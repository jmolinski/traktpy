# flake8: noqa: F403, F405
from dataclasses import dataclass
from typing import Any

import pytest
from trakt.core import json_parser


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
