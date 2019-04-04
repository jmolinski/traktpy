import pytest
from tests.test_data.movies import (
    ALIASES,
    ANTICIPATED_MOVIES,
    BOX_OFFICE,
    EXTENDED_MOVIE,
    MOVIES,
    PLAYED_MOVIES,
    RELEASES,
    TRENDING_MOVIES,
    UPDATED_MOVIES,
)
from tests.utils import mk_mock_client
from trakt.core.exceptions import ArgumentError

#  160-161, 166-170, 175-179, 184-185, 195-196, 199, 202, 207, 210, 215, 218-223


@pytest.fixture
def movies_client():
    PAG_H = {"X-Pagination-Page-Count": 1}
    return mk_mock_client(
        {
            r".*movies/trending.*": [TRENDING_MOVIES, 200, PAG_H],
            r".*movies/popular.*": [MOVIES, 200, PAG_H],
            r".*movies/played.*": [PLAYED_MOVIES, 200, PAG_H],
            r".*movies/watched.*": [PLAYED_MOVIES, 200, PAG_H],
            r".*movies/collected.*": [PLAYED_MOVIES, 200, PAG_H],
            r".*movies/anticipated.*": [ANTICIPATED_MOVIES, 200, PAG_H],
            r".*movies/boxoffice.*": [BOX_OFFICE, 200],
            r".*movies/updates.*": [UPDATED_MOVIES, 200, PAG_H],
            r".*movies/.*/aliases.*": [ALIASES, 200],
            r".*movies/.*/releases.*": [RELEASES, 200],
        }
    )


def test_trending(movies_client):
    movies = list(movies_client.movies.get_trending())

    assert len(movies) == 2
    assert movies[0].watchers == TRENDING_MOVIES[0]["watchers"]


def test_popular(movies_client):
    movies = list(movies_client.movies.get_popular())

    assert len(movies) == 2
    assert movies[0].title == MOVIES[0]["title"]


def test_played(movies_client):
    movies = list(movies_client.movies.get_most_played(countries="us", period="weekly"))

    assert len(movies) == 2
    assert movies[0].watcher_count == PLAYED_MOVIES[0]["watcher_count"]

    with pytest.raises(ArgumentError):
        movies_client.movies.get_most_played(countries="xyz")

    with pytest.raises(ArgumentError):
        movies_client.movies.get_most_played(period="xyz")


def test_watched(movies_client):
    movies = list(movies_client.movies.get_most_watched(genres="de"))
    assert movies[0].play_count == PLAYED_MOVIES[0]["play_count"]


def test_collected(movies_client):
    movies = list(movies_client.movies.get_most_collected(period="all"))
    assert movies[0].movie.title == PLAYED_MOVIES[0]["movie"]["title"]


def test_anticipated(movies_client):
    movies = list(movies_client.movies.get_most_anticipated())
    assert movies[0].list_count == ANTICIPATED_MOVIES[0]["list_count"]


def test_box_office(movies_client):
    movies = list(movies_client.movies.get_box_office())
    assert movies[0].revenue == BOX_OFFICE[0]["revenue"]


def test_updated(movies_client):
    movies = list(movies_client.movies.get_recently_updated(start_date="2012-05-05"))
    assert movies[0].movie.title == UPDATED_MOVIES[0]["movie"]["title"]

    with pytest.raises(ArgumentError):
        movies_client.movies.get_recently_updated(start_date="2012-14-5")


def test_summary():
    client = mk_mock_client({".*movies.*": [EXTENDED_MOVIE, 200]})

    movie = client.movies.get_summary(movie=123, extended=True)

    assert movie.homepage == EXTENDED_MOVIE["homepage"]


def test_aliases(movies_client):
    aliases = movies_client.movies.get_aliases(movie=123)
    assert aliases[0].title == ALIASES[0]["title"]


def test_releases(movies_client):
    releases = movies_client.movies.get_releases(movie=123, country="us")
    assert releases[0].release_type == RELEASES[0]["release_type"]
