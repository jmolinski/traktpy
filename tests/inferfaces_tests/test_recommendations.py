from datetime import date

import pytest
from tests.test_data.calendars import MOVIE_PREMIERES, SEASON_PREMIERES, SHOWS
from tests.test_data.movies import MOVIE1, MOVIE2, MOVIES
from tests.utils import USER, mk_mock_client
from trakt.core.exceptions import ArgumentError, NotAuthenticated


def test_recommendations_movies():
    client = mk_mock_client(
        {r".*movies?ignore_collected=true": [MOVIES, 200]}, user=None
    )

    with pytest.raises(NotAuthenticated):
        client.recommendations.get_movie_recommendations()

    client.set_user(USER)

    with pytest.raises(ArgumentError):
        client.recommendations.get_movie_recommendations(ignore_collected=5)

    movies = client.recommendations.get_movie_recommendations(ignore_collected=True)

    print(movies)
