import pytest
from tests.test_data.comments import COMMENTS
from tests.test_data.episodes import EXTENDED_EPISODE
from tests.test_data.lists import LIST
from tests.test_data.movies import RATINGS
from tests.test_data.shows import SHOW_STATS, TRANSLATIONS
from tests.test_data.user import USER
from tests.utils import mk_mock_client


@pytest.fixture
def episodes_client():
    PAG_H = {"X-Pagination-Page-Count": 1}
    return mk_mock_client(
        {
            r".*episodes/.*/translations.*": [TRANSLATIONS, 200],
            r".*episodes/.*/comments.*": [COMMENTS, 200, PAG_H],
            r".*episodes/.*/lists.*": [[LIST], 200, PAG_H],
            r".*episodes/.*/ratings.*": [RATINGS, 200],
            r".*episodes/.*/stats.*": [SHOW_STATS, 200],
            r".*episodes/.*/watching.*": [[USER], 200],
        }
    )


def test_summary():
    client = mk_mock_client({".*episodes.*": [EXTENDED_EPISODE, 200]})
    episode = client.episodes.get_episode(show=1, season=1, episode=1, extended=True)

    assert episode.title == EXTENDED_EPISODE["title"]


def test_translations(episodes_client):
    translations = episodes_client.episodes.get_translations(
        show=1, season=1, episode=1, language="de"
    )
    assert translations[0].title == TRANSLATIONS[0]["title"]


def test_comments(episodes_client):
    comments = list(episodes_client.episodes.get_comments(show=1, season=1, episode=1))
    assert comments[0].comment == COMMENTS[0]["comment"]


def test_lists(episodes_client):
    lists = list(episodes_client.episodes.get_lists(show=123, season=1, episode=1))
    assert lists[0].comment_count == LIST["comment_count"]


def test_ratings(episodes_client):
    ratings = episodes_client.episodes.get_ratings(show=123, season=1, episode=1)
    assert ratings.rating == RATINGS["rating"]


def test_stats(episodes_client):
    stats = episodes_client.episodes.get_stats(show=123, season=1, episode=1)
    assert stats.watchers == SHOW_STATS["watchers"]


def test_watching(episodes_client):
    watching = list(
        episodes_client.episodes.get_users_watching(show=123, season=1, episode=1)
    )
    assert watching[0].name == USER["name"]
