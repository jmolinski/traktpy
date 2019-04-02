from tests.test_data.user import USER

LIST = {
    "name": "Incredible Thoughts",
    "description": "How could my brain conceive them?",
    "privacy": "public",
    "display_numbers": True,
    "allow_comments": True,
    "sort_by": "rank",
    "sort_how": "asc",
    "created_at": "2014-10-11T17:00:54.000Z",
    "updated_at": "2014-10-11T17:00:54.000Z",
    "item_count": 50,
    "comment_count": 10,
    "likes": 99,
    "ids": {"trakt": 1337, "slug": "incredible-thoughts"},
    "user": USER,
}

TRENDING_LISTS = [{"like_count": 5, "comment_count": 5, "list": LIST, "user": USER}]
TRENDING_LISTS_MISSING_DATA = [{"comment_count": 5, "list": LIST, "user": USER}]
