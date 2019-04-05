import pytest
from tests.test_data.comments import COMMENTS
from tests.test_data.lists import LIST
from tests.test_data.movies import (
    ALIASES,
    ANTICIPATED_MOVIES,
    BOX_OFFICE,
    EXTENDED_MOVIE,
    MOVIE_STATS,
    MOVIES,
    PLAYED_MOVIES,
    RATINGS,
    RELATED_MOVIES,
    RELEASES,
    TRANSLATIONS,
    TRENDING_MOVIES,
    UPDATED_MOVIES,
)
from tests.test_data.people import MOVIE_ALL_PEOPLE
from tests.test_data.user import USER
from tests.utils import mk_mock_client
from trakt.core.exceptions import ArgumentError


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
            r".*movies/.*/translations.*": [TRANSLATIONS, 200],
            r".*movies/.*/comments.*": [COMMENTS, 200, PAG_H],
            r".*movies/.*/lists.*": [[LIST], 200, PAG_H],
            r".*movies/.*/people.*": [MOVIE_ALL_PEOPLE, 200, PAG_H],
            r".*movies/.*/ratings.*": [RATINGS, 200],
            r".*movies/.*/related.*": [RELATED_MOVIES, 200, PAG_H],
            r".*movies/.*/stats.*": [MOVIE_STATS, 200],
            r".*movies/.*/watching.*": [[USER], 200],
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


def test_translations(movies_client):
    translations = movies_client.movies.get_translations(movie=123, language="de")
    assert translations[0].title == TRANSLATIONS[0]["title"]


def test_comments(movies_client):
    with pytest.raises(ArgumentError):
        movies_client.movies.get_comments(movie=123, sort="xtz")

    comments = list(movies_client.movies.get_comments(movie=123))
    assert comments[0].comment == COMMENTS[0]["comment"]


def test_lists(movies_client):
    lists = list(movies_client.movies.get_lists(movie=123))
    assert lists[0].comment_count == LIST["comment_count"]


def test_get_people(movies_client):
    people = movies_client.movies.get_people(movie=123)
    assert people.cast[0].character == MOVIE_ALL_PEOPLE["cast"][0]["character"]


def test_ratings(movies_client):
    ratings = movies_client.movies.get_ratings(movie=123)
    assert ratings.rating == RATINGS["rating"]


def test_related(movies_client):
    related = list(movies_client.movies.get_related(movie=123))
    assert related[0].title == RELATED_MOVIES[0]["title"]


def test_stats(movies_client):
    stats = movies_client.movies.get_stats(movie=123)
    assert stats.watchers == MOVIE_STATS["watchers"]


def test_watching(movies_client):
    watching = list(movies_client.movies.get_users_watching(movie=123))
    assert watching[0].name == USER["name"]
