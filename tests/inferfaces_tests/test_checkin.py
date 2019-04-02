import pytest
from tests.test_data.checkin import CHECKIN_EPISODE, CHECKIN_MOVIE
from tests.utils import USER, mk_mock_client
from trakt.core.exceptions import ArgumentError, NotAuthenticated
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

    client.checkin.check_into_episode(episode="eid", shows={"ids": {"trakt": "123"}})


def test_dispatch():
    client = mk_mock_client({r".*checkin.*": [CHECKIN_EPISODE, 201]})

    with pytest.raises(ArgumentError):
        client.checkin.check_into()

    with pytest.raises(ArgumentError):
        client.checkin.check_into(episode="eid", movie="eid")

    client.checkin.check_into(episode="eid")

    client = mk_mock_client({r".*checkin.*": [CHECKIN_MOVIE, 201]})
    client.checkin.check_into(movie="eid")
