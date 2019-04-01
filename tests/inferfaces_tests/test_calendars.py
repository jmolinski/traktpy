from datetime import date

import pytest
from tests.client import get_mock_http_component
from tests.test_data.calendars import MOVIE_PREMIERES, SEASON_PREMIERES, SHOWS
from trakt import Trakt, TraktCredentials
from trakt.core.exceptions import NotAuthenticated

USER = TraktCredentials("", "", "", 10e14)


def test_shows():
    http = get_mock_http_component({r".*calendars/.*/shows.*": [SHOWS, 200]})
    client = Trakt("", "", http_component=http)

    with pytest.raises(NotAuthenticated):
        client.calendars.get_my_shows()

    shows = client.calendars.get_shows()
    client.set_user(USER)
    my_shows = client.calendars.get_my_shows(start_date="2014-09-01", days=7)

    assert my_shows == shows


def test_new_shows():
    http = get_mock_http_component({r".*calendars/(my|all)/shows/new.*": [SHOWS, 200]})
    client = Trakt("", "", http_component=http)

    with pytest.raises(NotAuthenticated):
        client.calendars.get_my_new_shows()

    shows = client.calendars.get_new_shows(extended=True)
    client.set_user(USER)
    my_shows = client.calendars.get_my_new_shows(start_date="2014-09-01", days=7)

    assert my_shows == shows


def test_season_premieres():
    http = get_mock_http_component(
        {r".*calendars/(my|all)/shows/premieres.*": [SEASON_PREMIERES, 200]}
    )
    client = Trakt("", "", http_component=http, user=USER)

    premieres = client.calendars.get_season_premieres()
    my_premieres = client.calendars.get_my_season_premieres()

    assert premieres == my_premieres

    assert len(premieres) == 1

    premiere = premieres[0]

    assert premiere.first_aired
    assert premiere.episode.title == "Episode 1"
    assert premiere.show.title == "Make Or Break?"


def test_movies():
    http = get_mock_http_component(
        {r".*calendars/(my|all)/movies.*": [MOVIE_PREMIERES, 200]}
    )
    client = Trakt("", "", http_component=http, user=USER)

    movies = client.calendars.get_movies()
    my_movies = client.calendars.get_my_movies()

    assert movies == my_movies
    assert len(movies) == 2
    assert movies[0].released == date(2014, 8, 1)


def test_dvd():
    http = get_mock_http_component(
        {r".*calendars/(my|all)/dvd.*": [MOVIE_PREMIERES, 200]}
    )
    client = Trakt("", "", http_component=http, user=USER)

    dvd = client.calendars.get_dvd_releases()
    my_dvd = client.calendars.get_my_dvd_releases()

    assert dvd == my_dvd
