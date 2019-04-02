from datetime import date

import pytest
from tests.test_data.calendars import MOVIE_PREMIERES, SEASON_PREMIERES, SHOWS
from tests.utils import USER, mk_mock_client
from trakt.core.exceptions import NotAuthenticated


def test_shows():
    client = mk_mock_client({r".*calendars/.*/shows.*": [SHOWS, 200]}, user=None)

    with pytest.raises(NotAuthenticated):
        client.calendars.get_my_shows()

    shows = client.calendars.get_shows()
    client.set_user(USER)
    my_shows = client.calendars.get_my_shows(start_date="2014-09-01", days=7)

    assert my_shows == shows


def test_new_shows():
    client = mk_mock_client(
        {r".*calendars/(my|all)/shows/new.*": [SHOWS, 200]}, user=None
    )

    with pytest.raises(NotAuthenticated):
        client.calendars.get_my_new_shows()

    shows = client.calendars.get_new_shows(extended=True)
    client.set_user(USER)
    my_shows = client.calendars.get_my_new_shows(start_date="2014-09-01", days=7)

    assert my_shows == shows


def test_season_premieres():
    client = mk_mock_client(
        {r".*calendars/(my|all)/shows/premieres.*": [SEASON_PREMIERES, 200]}
    )

    premieres = client.calendars.get_season_premieres()
    my_premieres = client.calendars.get_my_season_premieres()

    assert premieres == my_premieres

    assert len(premieres) == 1

    premiere = premieres[0]

    assert premiere.first_aired
    assert premiere.episode.title == "Episode 1"
    assert premiere.show.title == "Make Or Break?"


def test_movies():
    client = mk_mock_client({r".*calendars/(my|all)/movies.*": [MOVIE_PREMIERES, 200]})

    movies = client.calendars.get_movies()
    my_movies = client.calendars.get_my_movies()

    assert movies == my_movies
    assert len(movies) == 2
    assert movies[0].released == date(2014, 8, 1)


def test_dvd():
    client = mk_mock_client({r".*calendars/(my|all)/dvd.*": [MOVIE_PREMIERES, 200]})

    dvd = client.calendars.get_dvd_releases()
    my_dvd = client.calendars.get_my_dvd_releases()

    assert dvd == my_dvd
