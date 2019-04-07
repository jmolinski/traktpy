from tests.test_data.movies import MOVIE1
from tests.test_data.shows import SHOW
from tests.test_data.user import USER

COMMENT = {
    "id": 8,
    "parent_id": 0,
    "created_at": "2011-03-25T22:35:17.000Z",
    "updated_at": "2011-03-25T22:35:17.000Z",
    "comment": "Great movie!",
    "spoiler": False,
    "review": False,
    "replies": 1,
    "likes": 0,
    "user_rating": 8,
    "user": {
        "username": "sean",
        "private": False,
        "name": "Sean Rudford",
        "vip": True,
        "vip_ep": False,
        "ids": {"slug": "sean"},
    },
}

COMMENTS = [COMMENT]

ATTACHED_SHOW = {"type": "show", "show": SHOW}

LIKED_USER = {"liked_at": "2014-09-01T09:10:11.000Z", "user": USER}

TRENDING_COMMENTS = [{"type": "movie", "movie": MOVIE1, "comment": COMMENT}]
