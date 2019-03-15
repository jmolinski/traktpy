# flake8: noqa: F403, F405

from trakt import Trakt
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

    assert not p.is_valid(client)
    assert not p.is_valid(client)  # intentional, assert didn't bind any values

    assert p.is_valid(client, b=10)
    assert p.get_path_and_qargs() == ("aaa/10/ccc", {})
