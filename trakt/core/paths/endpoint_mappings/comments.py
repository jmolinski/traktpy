from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from trakt.core.models import Episode, Movie, Season, Show
from trakt.core.paths.path import Path
from trakt.core.paths.response_structs import (
    Comment,
    CommentAndItem,
    CommentItemOnly,
    CommentLiker,
    CommentResponse,
    Sharing,
)
from trakt.core.paths.suite_interface import SuiteInterface
from trakt.core.paths.validators import (
    AuthRequiredValidator,
    PerArgValidator,
    Validator,
)

if TYPE_CHECKING:  # pragma: no cover
    from trakt.core.executors import PaginationIterator

COMMENT_TEXT_VALIDATOR = PerArgValidator(
    "comment", lambda c: isinstance(c, str) and len(c.split(" ")) > 4
)
COMMENT_ID_VALIDATOR = PerArgValidator("id", lambda c: isinstance(c, int))

COMMENT_TYPES = ["all", "reviews", "shouts"]
MEDIA_TYPES = ["all", "movies", "shows", "seasons", "episodes", "lists"]

TRENDING_RECENT_UPDATED_VALIDATORS: List[Validator] = [
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
        "update_comment": Path(
            "comments/!id",
            Comment,
            methods="PUT",
            validators=[COMMENT_ID_VALIDATOR, COMMENT_TEXT_VALIDATOR],
        ),
        "delete_comment": Path(
            "comments/!id", {}, methods="DELETE", validators=[COMMENT_ID_VALIDATOR]
        ),
        "get_replies": Path(
            "comments/!id/replies",
            [Comment],
            validators=[COMMENT_ID_VALIDATOR],
            pagination=True,
        ),
        "post_reply": Path(
            "comments/!id/replies",
            Comment,
            validators=[
                AuthRequiredValidator(),
                COMMENT_ID_VALIDATOR,
                COMMENT_TEXT_VALIDATOR,
            ],
        ),
        "get_item": Path(
            "comments/!id/item",
            CommentItemOnly,
            validators=[COMMENT_ID_VALIDATOR],
            extended=["full"],
        ),
        "get_likes": Path(
            "comments/!id/likes",
            [CommentLiker],
            validators=[COMMENT_ID_VALIDATOR],
            pagination=True,
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
        sharing: Optional[Union[Sharing, Dict[str, bool]]] = None,
        **kwargs
    ) -> CommentResponse:
        body: Dict[str, Union[str, int, Dict[str, bool]]] = {
            "item_id": self._generic_get_id(item),
            "comment": comment,
            "spoiler": spoiler,
        }
        if sharing:
            if isinstance(sharing, Sharing):
                sharing = asdict(sharing)
            body["sharing"] = sharing

        return self.run("post_comment", **kwargs, body=body, comment=comment)

    def get_comment(self, *, id: Union[Comment, str, int], **kwargs) -> Comment:
        id = int(self._generic_get_id(id))
        return self.run("get_comment", **kwargs, id=id)

    def update_comment(
        self,
        *,
        id: Union[Comment, str, int],
        comment: str,
        spoiler: bool = False,
        **kwargs
    ) -> Comment:
        body = {"id": self._generic_get_id(id), "comment": comment, "spoiler": spoiler}
        return self.run("update_comment", **kwargs, body=body, id=id, comment=comment)

    def delete_comment(self, *, id: Union[Comment, str, int], **kwargs) -> None:
        id = int(self._generic_get_id(id))
        self.run("delete_comment", **kwargs, id=id)

    def get_replies(
        self, *, id: Union[Comment, str, int], **kwargs
    ) -> PaginationIterator[Comment]:
        id = int(self._generic_get_id(id))
        return self.run("get_replies", **kwargs, id=id)

    def post_reply(
        self,
        *,
        id: Union[Comment, str, int],
        comment: str,
        spoiler: bool = False,
        **kwargs
    ) -> PaginationIterator[Comment]:
        id = int(self._generic_get_id(id))

        body = {"comment": comment, "spoiler": spoiler}

        return self.run("post_reply", **kwargs, id=id, body=body, comment=comment)

    def get_item(self, *, id: Union[Comment, str, int], **kwargs) -> CommentItemOnly:
        id = int(self._generic_get_id(id))
        return self.run("get_item", **kwargs, id=id)

    def get_likes(
        self, *, id: Union[Comment, str, int], **kwargs
    ) -> List[CommentLiker]:
        id = int(self._generic_get_id(id))
        return self.run("get_likes", **kwargs, id=id)

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
