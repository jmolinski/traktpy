import pytest
from tests.test_data.comments import COMMENTS
from tests.test_data.episodes import EXTENDED_EPISODE
from tests.test_data.lists import LIST
from tests.test_data.movies import ALIASES, RATINGS
from tests.test_data.people import MOVIE_ALL_PEOPLE
from tests.test_data.shows import (
    ANTICIPATED_SHOWS,
    COLLECTION_PROGRESS,
    EXTENDED_SHOW,
    PLAYED_SHOWS,
    RELATED_SHOWS,
    SHOW,
    SHOW_STATS,
    TRANSLATIONS,
    TRENDING_SHOWS,
    UPDATED_SHOWS,
    WATCHED_PROGRESS,
)
from tests.test_data.user import USER
from tests.utils import MockResponse, mk_mock_client
from trakt.core.exceptions import ArgumentError


@pytest.fixture
def shows_client():
    PAG_H = {"X-Pagination-Page-Count": 1}
    return mk_mock_client(
        {
            r".*shows/trending.*": [TRENDING_SHOWS, 200, PAG_H],
            r".*shows/popular.*": [[SHOW], 200, PAG_H],
            r".*shows/played.*": [PLAYED_SHOWS, 200, PAG_H],
            r".*shows/watched.*": [PLAYED_SHOWS, 200, PAG_H],
            r".*shows/collected.*": [PLAYED_SHOWS, 200, PAG_H],
            r".*shows/anticipated.*": [ANTICIPATED_SHOWS, 200, PAG_H],
            r".*shows/updates.*": [UPDATED_SHOWS, 200, PAG_H],
            r".*shows/.*/aliases.*": [ALIASES, 200],
            r".*shows/.*/translations.*": [TRANSLATIONS, 200],
            r".*shows/.*/comments.*": [COMMENTS, 200, PAG_H],
            r".*shows/.*/lists.*": [[LIST], 200, PAG_H],
            r".*shows/.*/progress/collection.*": [COLLECTION_PROGRESS, 200],
            r".*shows/.*/progress/watched.*": [WATCHED_PROGRESS, 200],
            r".*shows/.*/people.*": [MOVIE_ALL_PEOPLE, 200, PAG_H],
            r".*shows/.*/ratings.*": [RATINGS, 200],
            r".*shows/.*/related.*": [RELATED_SHOWS, 200, PAG_H],
            r".*shows/.*/stats.*": [SHOW_STATS, 200],
            r".*shows/.*/watching.*": [[USER], 200],
        }
    )


def test_trending(shows_client):
    shows = list(shows_client.shows.get_trending())

    assert len(shows) == 2
    assert shows[0].watchers == TRENDING_SHOWS[0]["watchers"]


def test_popular(shows_client):
    shows = list(shows_client.shows.get_popular())
    assert shows[0].ids.trakt == SHOW["ids"]["trakt"]


def test_played(shows_client):
    shows = list(shows_client.shows.get_most_played())
    assert shows[0].show.title == PLAYED_SHOWS[0]["show"]["title"]


def test_watched(shows_client):
    shows = list(shows_client.shows.get_most_watched())
    assert shows[0].show.year == PLAYED_SHOWS[0]["show"]["year"]


def test_collected(shows_client):
    shows = list(shows_client.shows.get_most_collected())
    assert shows[0].show.ids.slug == PLAYED_SHOWS[0]["show"]["ids"]["slug"]


def test_anticipated(shows_client):
    shows = list(shows_client.shows.get_most_anticipated())
    assert shows[0].list_count == ANTICIPATED_SHOWS[0]["list_count"]


def test_updated(shows_client):
    shows = list(shows_client.shows.get_recently_updated(start_date="2012-05-05"))
    assert shows[0].show.title == UPDATED_SHOWS[0]["show"]["title"]

    with pytest.raises(ArgumentError):
        shows_client.shows.get_recently_updated(start_date="2012-14-5")


def test_summary():
    client = mk_mock_client({".*shows.*": [EXTENDED_SHOW, 200]})
    show = client.shows.get_summary(show=123, extended=True)

    assert show.network == EXTENDED_SHOW["network"]


def test_aliases(shows_client):
    aliases = shows_client.shows.get_aliases(show=123)
    assert aliases[0].title == ALIASES[0]["title"]


def test_translations(shows_client):
    translations = shows_client.shows.get_translations(show=123, language="de")
    assert translations[0].title == TRANSLATIONS[0]["title"]


def test_comments(shows_client):
    with pytest.raises(ArgumentError):
        shows_client.shows.get_comments(show=123, sort="xtz")

    comments = list(shows_client.shows.get_comments(show=123))
    assert comments[0].comment == COMMENTS[0]["comment"]


def test_lists(shows_client):
    lists = list(shows_client.shows.get_lists(show=123))
    assert lists[0].comment_count == LIST["comment_count"]


def test_progress_collection(shows_client):
    progress = shows_client.shows.get_collection_progress(show=123)
    assert progress.aired == COLLECTION_PROGRESS["aired"]


def test_progress_watched(shows_client):
    progress = shows_client.shows.get_watched_progress(show=123)
    assert progress.completed == WATCHED_PROGRESS["completed"]


def test_get_people(shows_client):
    people = shows_client.shows.get_people(show=123)
    assert people.cast[0].character == MOVIE_ALL_PEOPLE["cast"][0]["character"]


def test_ratings(shows_client):
    ratings = shows_client.shows.get_ratings(show=123)
    assert ratings.rating == RATINGS["rating"]


def test_related(shows_client):
    related = list(shows_client.shows.get_related(show=123))
    assert related[0].title == RELATED_SHOWS[0]["title"]


def test_stats(shows_client):
    stats = shows_client.shows.get_stats(show=123)
    assert stats.watchers == SHOW_STATS["watchers"]


def test_watching(shows_client):
    watching = list(shows_client.shows.get_users_watching(show=123))
    assert watching[0].name == USER["name"]


def test_next_episode():
    def next_ep_responses():
        yield MockResponse({}, 204)
        yield MockResponse(EXTENDED_EPISODE, 200)

    client = mk_mock_client({".*shows.*": next_ep_responses()})

    no_ep = client.shows.get_next_episode(show=123, extended=True)
    ep = client.shows.get_next_episode(show=123, extended=True)

    assert no_ep is None
    assert ep.runtime == EXTENDED_EPISODE["runtime"]


def test_last_episode():
    def next_ep_responses():
        yield MockResponse({}, 204)
        yield MockResponse(EXTENDED_EPISODE, 200)

    client = mk_mock_client({".*shows.*": next_ep_responses()})

    no_ep = client.shows.get_last_episode(show=123, extended=True)
    ep = client.shows.get_last_episode(show=123, extended=True)

    assert no_ep is None
    assert ep.overview == EXTENDED_EPISODE["overview"]
