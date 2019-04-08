from tests.test_data.episodes import EPISODE
from tests.test_data.movies import MOVIE1
from tests.test_data.shows import SHOW

RESP_MOVIE = {
    "id": 0,
    "action": "start",
    "progress": 1.25,
    "sharing": {"twitter": True, "tumblr": False},
    "movie": MOVIE1,
}

RESP_EPISODE = {
    "id": 0,
    "action": "start",
    "progress": 10,
    "sharing": {"twitter": True, "tumblr": False},
    "episode": EPISODE,
    "show": SHOW,
}
