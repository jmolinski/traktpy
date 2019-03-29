# flake8: noqa: F401

from typing import Any, Iterable, List, Optional, Union

from trakt.core.exceptions import ArgumentError
from trakt.core.json_parser import parse_tree
from trakt.core.models import Episode, Movie, Season, Show, TraktList
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    Comment,
    CommentAndItem,
    CommentItemOnly,
    CommentResponse,
    Sharing,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import AuthRequiredValidator, PerArgValidator

COMMENT_TEXT_VALIDATOR = PerArgValidator(
    "comment", lambda c: isinstance(c, str) and len(c.split(" ")) > 4
)
COMMENT_ID_VALIDATOR = PerArgValidator("id", lambda c: isinstance(c, int))

COMMENT_TYPES = ["all", "reviews", "shouts"]
MEDIA_TYPES = ["all", "movies", "shows", "seasons", "episodes", "lists"]

TRENDING_RECENT_UPDATED_VALIDATORS = [
    PerArgValidator("comment_type", lambda c: c in COMMENT_TYPES),
    PerArgValidator("type", lambda c: c in MEDIA_TYPES),
    PerArgValidator("include_replies", lambda i: isinstance(i, bool)),
]


class CommentsI(SuiteInterface):
    name = "comments"

    paths = {
        "post_comment": Path(
            "comments",
            CommentResponse,
            methods=["POST"],
            validators=[AuthRequiredValidator(), COMMENT_TEXT_VALIDATOR],
        ),
        "get_comment": Path("comments/!id", Comment, validators=[COMMENT_ID_VALIDATOR]),
        "get_replies": Path(
            "comments/!id/replies",
            [Comment],
            validators=[COMMENT_ID_VALIDATOR],
            pagination=True,
        ),
        "post_reply": Path(
            "comments/!id/replies",
            [Comment],
            validators=[
                AuthRequiredValidator(),
                COMMENT_ID_VALIDATOR,
                COMMENT_TEXT_VALIDATOR,
            ],
            pagination=True,
        ),
        "get_item": Path(
            "comments/!id/item",
            Any,
            validators=[COMMENT_ID_VALIDATOR],
            extended=["full"],
        ),
        "like_comment": Path(
            "comments/!id/like",
            {},
            methods=["POST"],
            validators=[AuthRequiredValidator(), COMMENT_ID_VALIDATOR],
        ),
        "remove_like": Path(
            "comments/!id/like",
            {},
            methods=["DELETE"],
            validators=[AuthRequiredValidator(), COMMENT_ID_VALIDATOR],
        ),
        "get_trending": Path(
            "comments/trending/?comment_type/?type",
            [CommentAndItem],
            validators=TRENDING_RECENT_UPDATED_VALIDATORS,
            pagination=True,
            extended=["full"],
        ),
        "get_recently_created": Path(
            "comments/recent/?comment_type/?type",
            [CommentAndItem],
            validators=TRENDING_RECENT_UPDATED_VALIDATORS,
            pagination=True,
            extended=["full"],
        ),
        "get_recently_updated": Path(
            "comments/updates/?comment_type/?type",
            [CommentAndItem],
            validators=TRENDING_RECENT_UPDATED_VALIDATORS,
            pagination=True,
            extended=["full"],
        ),
    }

    def post_comment(
        self,
        *,
        item: Union[str, int, Movie, Season, Show, Episode],
        comment: str,
        spoiler: bool = False,
        sharing: Optional[Sharing] = None,
        **kwargs
    ) -> CommentResponse:
        body = {
            "item_id": self._generic_get_id(item),
            "comment": comment,
            "spoiler": spoiler,
        }
        if sharing:
            body["sharing"] = sharing

        return self.run("post_comment", **kwargs, body=body, comment=comment)

    def get_comment(self, *, id: Union[Comment, str, int], **kwargs) -> Comment:
        id = int(self._generic_get_id(id))
        return self.run("get_comment", **kwargs, id=id)

    def get_replies(
        self, *, id: Union[Comment, str, int], **kwargs
    ) -> Iterable[Comment]:
        id = int(self._generic_get_id(id))
        return self.run("get_replies", **kwargs, id=id)

    def post_reply(
        self,
        *,
        id: Union[Comment, str, int],
        comment: str,
        spoiler: bool = False,
        **kwargs
    ) -> Iterable[Comment]:
        id = int(self._generic_get_id(id))

        body = {"comment": comment, "spoiler": spoiler}

        return self.run("post_reply", **kwargs, id=id, body=body, comment=comment)

    def get_item(
        self, *, id: Union[Comment, str, int], **kwargs
    ) -> Union[Show, TraktList, Episode, Movie, Season]:
        id = int(self._generic_get_id(id))

        response = self.run("get_item", **kwargs, id=id)

        ret_types = {
            "show": Show,
            "list": TraktList,
            "episode": Episode,
            "season": Season,
            "movie": Movie,
        }

        type, data = response["type"], response[response["type"]]
        ret_type = ret_types[type]

        return parse_tree(data, ret_type)

    def like_comment(self, *, id: Union[Comment, str, int], **kwargs) -> None:
        id = int(self._generic_get_id(id))
        self.run("like_comment", **kwargs, id=id)

    def remove_like(self, *, id: Union[Comment, str, int], **kwargs) -> None:
        id = int(self._generic_get_id(id))
        self.run("remove_like", **kwargs, id=id)

    def get_trending(
        self,
        *,
        comment_type: str = "all",
        type: str = "all",
        include_replies: bool = False,
        **kwargs
    ) -> List[CommentAndItem]:
        return self.run(
            "get_trending",
            **kwargs,
            comment_type=comment_type,
            type=type,
            include_replies=include_replies
        )

    def get_recently_created(
        self,
        *,
        comment_type: str = "all",
        type: str = "all",
        include_replies: bool = False,
        **kwargs
    ) -> List[CommentAndItem]:
        return self.run(
            "get_recently_created",
            **kwargs,
            comment_type=comment_type,
            type=type,
            include_replies=include_replies
        )

    def get_recently_updated(
        self,
        *,
        comment_type: str = "all",
        type: str = "all",
        include_replies: bool = False,
        **kwargs
    ) -> List[CommentAndItem]:
        return self.run(
            "get_recently_updated",
            **kwargs,
            comment_type=comment_type,
            type=type,
            include_replies=include_replies
        )
