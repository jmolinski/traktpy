import pytest
from tests.test_data.movies import MOVIE1, MOVIES
from tests.test_data.shows import SHOW
from tests.utils import USER, mk_mock_client
from trakt.core.exceptions import ArgumentError, NotAuthenticated
from trakt.core.json_parser import parse_tree
from trakt.core.models import Movie, Show


def test_recommendations_movies():
    client = mk_mock_client(
        {r".*movies\?ignore_collected=true": [MOVIES, 200]}, user=None
    )

    with pytest.raises(NotAuthenticated):
        client.recommendations.get_movie_recommendations()

    client.set_user(USER)

    with pytest.raises(ArgumentError):
        client.recommendations.get_movie_recommendations(ignore_collected=5)

    movies = client.recommendations.get_movie_recommendations(ignore_collected=True)

    assert len(movies) == 2


def test_hide_movie():
    m_id = MOVIE1["ids"]["trakt"]
    client = mk_mock_client({rf".*movies/{m_id}": [{}, 204]}, user=None)

    movie = parse_tree(MOVIE1, tree_structure=Movie)

    with pytest.raises(NotAuthenticated):
        client.recommendations.hide_movie(movie=movie)

    client.set_user(USER)

    client.recommendations.hide_movie(movie=movie)
    client.recommendations.hide_movie(movie=movie.ids["trakt"])

    reqs = list(client.http._requests.req_map.items())[0]
    req = reqs[1][1]  # [(path, data)] -> data

    assert req["method"] == "DELETE"


def test_recommendations_shows():
    client = mk_mock_client(
        {r".*shows\?ignore_collected=true": [[SHOW], 200]}, user=None
    )

    with pytest.raises(NotAuthenticated):
        client.recommendations.get_show_recommendations()

    client.set_user(USER)
    shows = client.recommendations.get_show_recommendations(ignore_collected=True)

    assert len(shows) == 1


def test_hide_show():
    m_id = SHOW["ids"]["trakt"]
    client = mk_mock_client({rf".*shows/{m_id}": [{}, 204]}, user=None)

    show = parse_tree(SHOW, tree_structure=Show)

    with pytest.raises(NotAuthenticated):
        client.recommendations.hide_show(show=show)

    client.set_user(USER)

    client.recommendations.hide_show(show=show)

    reqs = list(client.http._requests.req_map.items())[0]
    req = reqs[1][0]  # [(path, data)] -> data

    assert req["method"] == "DELETE"
