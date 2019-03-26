# flake8: noqa: F403, F405
import pytest
from trakt import Trakt
from trakt.core.exceptions import ArgumentError
from trakt.core.paths.path import Path


def test_aliases():
    p = Path("a/b/c", {}, aliases=["", "xyz"])

    assert p.does_match("xyz")
    assert p.does_match("")
    assert not p.does_match("a")


def test_optional_args():
    client = Trakt("", "")

    p = Path("calendars/all/shows/new/?start_date/?days", [{"a": str}])

    assert p.methods == ["GET"]
    assert p.args == ["?start_date", "?days"]

    default_alias = "calendars.all.shows.new"

    assert p.aliases == [default_alias]
    assert p.does_match(default_alias)
    assert not p.does_match(default_alias[1:])

    assert p.is_valid(client)
    assert p.get_path_and_qargs() == ("calendars/all/shows/new", {})

    assert p.is_valid(client, start_date="2018-10-10")
    assert p.get_path_and_qargs() == ("calendars/all/shows/new/2018-10-10", {})


def test_required_args():
    client = Trakt("", "")

    p = Path("aaa/!b/ccc/?d", [{"a": str}])

    assert p.methods == ["GET"]
    assert p.args == ["!b", "?d"]

    default_alias = "aaa.ccc"

    assert p.aliases == [default_alias]
    assert p.does_match(default_alias)

    with pytest.raises(ArgumentError):
        p.is_valid(client)

    with pytest.raises(ArgumentError):  # intentional, assert didn't bind any values
        p.is_valid(client)

    assert p.is_valid(client, b=10)
    assert p.get_path_and_qargs() == ("aaa/10/ccc", {})


def test_extended():
    client = Trakt("", "")

    p = Path("a", {}, extended=["full"])

    assert p.is_valid(client)
    assert p.is_valid(client, extended="full")
    assert p.is_valid(client, extended=True)

    with pytest.raises(ArgumentError):
        p.is_valid(client, extended="meta")

    p.is_valid(client, extended=True)
    _, quargs = p.get_path_and_qargs()
    assert "extended" in quargs and quargs["extended"] == "full"

    p = Path("a", {})
    p.is_valid(client)
    _, quargs = p.get_path_and_qargs()
    assert "extended" not in quargs


def test_filters():
    client = Trakt("", "")
    p = Path("a", {})

    with pytest.raises(ArgumentError):
        p.is_valid(client, genres="genre")

    p = Path("a", {}, filters={"query", "genres"})

    assert p.is_valid(client, query="xyz")

    with pytest.raises(ArgumentError):
        p.is_valid(client, query=["xyz", "abc"])

    assert p.is_valid(client, genres="genre")
    assert p.is_valid(client, genres=["abc", "xyz"])

    with pytest.raises(ArgumentError):
        p.is_valid(client, query=[100, "abc"])


def test_get_quargs():
    client = Trakt("", "")
    p = Path("a", {}, filters={"query", "genres"}, extended=["metadata"])

    assert p.is_valid(client, extended=True, query="xyz", genres=["a", "b"])

    _, quargs = p.get_path_and_qargs()

    expected = {"genres": "a,b", "query": "xyz", "extended": "metadata"}

    assert quargs == expected
