import pytest
from tests.test_data.checkin import CHECKIN_EPISODE, CHECKIN_MOVIE
from tests.test_data.episodes import EPISODE
from tests.test_data.movies import MOVIE1
from tests.test_data.shows import SHOW
from tests.utils import USER, mk_mock_client
from trakt.core.exceptions import ArgumentError, NotAuthenticated
from trakt.core.json_parser import parse_tree
from trakt.core.models import Episode, Movie, Show
from trakt.core.paths.response_structs import Sharing


def test_movie_arg_validation():
    client = mk_mock_client({r".*checkin.*": [CHECKIN_MOVIE, 201]}, user=None)

    with pytest.raises(NotAuthenticated):
        client.checkin.check_into()

    with pytest.raises(NotAuthenticated):
        client.checkin.check_into_movie(movie="mid")

    client.set_user(USER)

    with pytest.raises(TypeError):
        client.checkin.check_into_movie()

    with pytest.raises(ArgumentError):
        client.checkin.check_into_movie(movie="eid", sharing=True)

    client.checkin.check_into_movie(movie="eid", sharing={"twitter": True})
    client.checkin.check_into_movie(
        movie="eid", sharing=Sharing(medium=True, twitter=False)
    )

    with pytest.raises(ArgumentError):
        client.checkin.check_into_movie(movie="eid", message=55)

    movie = parse_tree(MOVIE1, Movie)
    client.checkin.check_into_movie(movie=movie)


def test_episode_arg_validation():
    client = mk_mock_client({r".*checkin.*": [CHECKIN_EPISODE, 201]}, user=None)

    with pytest.raises(NotAuthenticated):
        client.checkin.check_into()

    with pytest.raises(NotAuthenticated):
        client.checkin.check_into_episode(episode="eid")

    client.set_user(USER)

    with pytest.raises(TypeError):
        client.checkin.check_into_episode()

    with pytest.raises(ArgumentError):
        client.checkin.check_into_episode(episode="eid", sharing=True)

    client.checkin.check_into_episode(episode="eid", sharing={"twitter": True})
    client.checkin.check_into_episode(
        episode="eid", sharing=Sharing(medium=True, twitter=False)
    )

    with pytest.raises(ArgumentError):
        client.checkin.check_into_episode(episode="eid", show=True)

    client.checkin.check_into_episode(episode="eid", show={"ids": {"trakt": "123"}})

    episode, show = parse_tree(EPISODE, Episode), parse_tree(SHOW, Show)
    client.checkin.check_into_episode(episode=episode, show=show)


def test_dispatch():
    client = mk_mock_client({r".*checkin.*": [CHECKIN_EPISODE, 201]})

    with pytest.raises(ArgumentError):
        client.checkin.check_into()

    with pytest.raises(ArgumentError):
        client.checkin.check_into(episode="eid", movie="eid")

    client.checkin.check_into(episode="eid")

    client = mk_mock_client({r".*checkin.*": [CHECKIN_MOVIE, 201]})
    client.checkin.check_into(movie="eid")


def test_delete_checkins():
    client = mk_mock_client({r".*checkin.*": [{}, 201]}, user=None)

    with pytest.raises(NotAuthenticated):
        client.checkin.delete_active_checkins()

    client.set_user(USER)

    client.checkin.delete_active_checkins()
