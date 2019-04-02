# flake8: noqa: F401
from tests.test_data.episodes import EPISODE, EXTENDED_EPISODE
from tests.test_data.movies import MOVIE_PREMIERES
from tests.test_data.shows import EXTENDED_SHOW, SHOW

SEASON_PREMIERES = [
    {"first_aired": "2019-02-01T00:00:00.000Z", "episode": EPISODE, "show": SHOW}
]

SEASON_PREMIERES_EXTENDED = [
    {
        "first_aired": "2019-02-01T00:00:00.000Z",
        "episode": EXTENDED_EPISODE,
        "show": EXTENDED_SHOW,
    }
]

SHOWS = [{"first_aired": "2014-07-14T01:00:00.000Z", "episode": EPISODE, "show": SHOW}]
