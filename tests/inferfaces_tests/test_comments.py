import pytest
from tests.test_data.comments import (
    ATTACHED_SHOW,
    COMMENT,
    LIKED_USER,
    TRENDING_COMMENTS,
)
from tests.test_data.movies import MOVIE1
from tests.test_data.shows import SHOW
from tests.utils import get_last_req, mk_mock_client
from trakt.core.exceptions import ArgumentError
from trakt.core.json_parser import parse_tree
from trakt.core.paths.response_structs import Comment, Sharing

PAG_H = {"X-Pagination-Page-Count": 1}


@pytest.fixture
def comments_client():
    return mk_mock_client(
        {
            r".*comments/.*/item.*": [ATTACHED_SHOW, 200],
            r".*comments/.*/likes.*": [[LIKED_USER], 200, PAG_H],
            r".*comments/trending.*": [TRENDING_COMMENTS, 200, PAG_H],
            r".*comments/recent.*": [TRENDING_COMMENTS, 200, PAG_H],
            r".*comments/updates.*": [TRENDING_COMMENTS, 200, PAG_H],
        }
    )


def test_post_comment():
    client = mk_mock_client({".*comments.*": [COMMENT, 201]})
    text = "a b c d e f"  # at least 5 words
    sharing = Sharing(twitter=True)
    comment = client.comments.post_comment(
        item=123, comment=text, spoiler=True, sharing=sharing
    )

    assert comment.id == COMMENT["id"]


def test_get_comment():
    client = mk_mock_client({".*comments.*": [COMMENT, 200]})
    comment = parse_tree(COMMENT, Comment)
    comment = client.comments.get_comment(id=comment)

    assert comment.user.name == COMMENT["user"]["name"]


def test_update_comment():
    client = mk_mock_client({".*comments.*": [COMMENT, 200]})

    with pytest.raises(ArgumentError):
        client.comments.update_comment(id=123, comment="a b")

    comment = client.comments.update_comment(id=123, comment="a b c d e f")

    assert comment.replies == COMMENT["replies"]


def test_delete_comment():
    client = mk_mock_client({".*comments.*": [{}, 204]})
    client.comments.delete_comment(id=123)

    assert get_last_req(client.http)["method"] == "DELETE"


def test_get_replies():
    client = mk_mock_client({".*comments.*": [[COMMENT], 200, PAG_H]})
    comments = list(client.comments.get_replies(id=123))
    assert comments[0].id == COMMENT["id"]


def test_post_reply():
    client = mk_mock_client({".*comments.*": [COMMENT, 201]})
    reply = client.comments.post_reply(id=123, comment="a b c d e f")
    assert reply.id == COMMENT["id"]


def test_get_item(comments_client):
    item = comments_client.comments.get_item(id=123)

    assert item.type == "show"
    assert item.show.ids.trakt == SHOW["ids"]["trakt"]


def test_get_users(comments_client):
    likes = list(comments_client.comments.get_likes(id=123))
    assert likes[0].user.username == LIKED_USER["user"]["username"]


def test_like_comment():
    client = mk_mock_client({".*comments.*": [{}, 200]})
    client.comments.like_comment(id=50)

    assert get_last_req(client.http)["method"] == "POST"


def test_remove_like():
    client = mk_mock_client({".*comments.*": [{}, 204]})
    client.comments.remove_like(id=50)

    assert get_last_req(client.http)["method"] == "DELETE"


def test_trending(comments_client):
    comments = list(comments_client.comments.get_trending(include_replies=True))
    assert comments[0].type == "movie"


def test_recently_created(comments_client):
    comments = list(comments_client.comments.get_recently_created(sort="newest"))
    assert comments[0].movie.title == MOVIE1["title"]


def test_recently_updated(comments_client):
    comments = list(comments_client.comments.get_recently_updated(type="movies"))
    assert comments[0].comment.id == TRENDING_COMMENTS[0]["comment"]["id"]
