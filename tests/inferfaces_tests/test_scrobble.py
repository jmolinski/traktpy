import pytest
from tests.test_data.scrobble import EPISODE, MOVIE1, RESP_EPISODE, RESP_MOVIE, SHOW
from tests.utils import mk_mock_client
from trakt.core.exceptions import ArgumentError
from trakt.core.json_parser import parse_tree
from trakt.core.models import Episode, Movie, Show


def test_start_scrobble_movie():
    client = mk_mock_client({".*scrobble.*": [RESP_MOVIE, 201]})

    movie = parse_tree(MOVIE1, Movie)
    episode = parse_tree(EPISODE, Episode)

    with pytest.raises(ArgumentError):
        client.scrobble.start_scrobble(progress=5)

    with pytest.raises(ArgumentError):
        client.scrobble.start_scrobble(progress=5, episode=episode, movie=movie)

    resp = client.scrobble.start_scrobble(movie=movie, progress=5)

    assert resp.movie.title == MOVIE1["title"]


def test_start_scrobble_episode():
    client = mk_mock_client({".*scrobble.*": [RESP_EPISODE, 201]})

    episode = parse_tree(EPISODE, Episode)
    show = parse_tree(SHOW, Show)
    resp = client.scrobble.start_scrobble(episode=episode, show=show, progress=5)

    assert resp.show.title == SHOW["title"]


def test_pause_scrobble_movie():
    client = mk_mock_client({".*scrobble.*": [RESP_MOVIE, 201]})

    movie = parse_tree(MOVIE1, Movie)
    episode = parse_tree(EPISODE, Episode)

    with pytest.raises(ArgumentError):
        client.scrobble.pause_scrobble(progress=5)

    with pytest.raises(ArgumentError):
        client.scrobble.pause_scrobble(progress=5, episode=episode, movie=movie)

    resp = client.scrobble.pause_scrobble(movie=movie, progress=5)

    assert resp.movie.title == MOVIE1["title"]


def test_pause_scrobble_episode():
    client = mk_mock_client({".*scrobble.*": [RESP_EPISODE, 201]})
    resp = client.scrobble.pause_scrobble(episode=123, show=123, progress=5)
    assert resp.show.title == SHOW["title"]


def test_stop_scrobble_movie():
    client = mk_mock_client({".*scrobble.*": [RESP_MOVIE, 201]})

    with pytest.raises(ArgumentError):
        client.scrobble.stop_scrobble(progress=5)

    with pytest.raises(ArgumentError):
        client.scrobble.stop_scrobble(progress=5, episode=123, movie=123)

    resp = client.scrobble.stop_scrobble(movie=123, progress=5)
    assert resp.movie.title == MOVIE1["title"]


def test_stop_scrobble_episode():
    client = mk_mock_client({".*scrobble.*": [RESP_EPISODE, 201]})
    resp = client.scrobble.stop_scrobble(episode=123, show=123, progress=5)
    assert resp.show.title == SHOW["title"]
