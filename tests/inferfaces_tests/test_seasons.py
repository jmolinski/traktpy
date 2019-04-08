import pytest
from tests.test_data.comments import COMMENTS
from tests.test_data.episodes import EXTENDED_EPISODE
from tests.test_data.lists import LIST
from tests.test_data.movies import RATINGS
from tests.test_data.seasons import SEASON
from tests.test_data.shows import SHOW_STATS
from tests.test_data.user import USER
from tests.utils import mk_mock_client


@pytest.fixture
def seasons_client():
    PAG_H = {"X-Pagination-Page-Count": 1}
    return mk_mock_client(
        {
            r".*seasons/.*/comments.*": [COMMENTS, 200, PAG_H],
            r".*seasons/.*/lists.*": [[LIST], 200, PAG_H],
            r".*seasons/.*/ratings.*": [RATINGS, 200],
            r".*seasons/.*/stats.*": [SHOW_STATS, 200],
            r".*seasons/.*/watching.*": [[USER], 200],
        }
    )


def test_summary():
    client = mk_mock_client({".*seasons.*": [[SEASON], 200]})
    seasons = list(client.seasons.get_all_seasons(show=1, season=1))

    assert seasons[0].number == SEASON["number"]


def test_detail():
    client = mk_mock_client({".*seasons.*": [[EXTENDED_EPISODE], 200]})
    episodes = client.seasons.get_season(show=1, season=1, extended="episodes")

    assert episodes[0].title == EXTENDED_EPISODE["title"]


def test_comments(seasons_client):
    comments = list(seasons_client.seasons.get_comments(show=1, season=1))
    assert comments[0].comment == COMMENTS[0]["comment"]


def test_lists(seasons_client):
    lists = list(seasons_client.seasons.get_lists(show=123, season=1))
    assert lists[0].comment_count == LIST["comment_count"]


def test_ratings(seasons_client):
    ratings = seasons_client.seasons.get_ratings(show=123, season=1)
    assert ratings.rating == RATINGS["rating"]


def test_stats(seasons_client):
    stats = seasons_client.seasons.get_stats(show=123, season=1)
    assert stats.watchers == SHOW_STATS["watchers"]


def test_watching(seasons_client):
    watching = list(seasons_client.seasons.get_users_watching(show=123, season=1))
    assert watching[0].name == USER["name"]
