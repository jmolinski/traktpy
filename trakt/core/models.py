from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import jsons  # type: ignore
from trakt.core.abstract import AbstractBaseModel

MediaForeignIDType = Union[int, str]


# TODO is there a way to do it better? currently not in use


def any_deserializer(obj: Any, *args, **kwargs) -> Any:
    return obj


jsons.set_deserializer(any_deserializer, Any)

#


@dataclass
class Show(AbstractBaseModel):
    title: str
    year: int
    ids: Any

    overview: str = ""
    first_aired: str = ""
    airs: Dict[str, Any] = field(default_factory=dict)
    runtime: int = 0
    certification: str = ""
    network: str = ""
    country: str = ""
    trailer: str = ""
    homepage: str = ""
    status: str = ""
    rating: int = 0
    votes: int = 0
    comment_count: int = 0
    updated_at: str = ""
    language: str = ""
    available_translations: List[str] = field(default_factory=list)
    genres: List[str] = field(default_factory=list)
    aired_episodes: int = 0


@dataclass
class User(AbstractBaseModel):
    username: str
    private: bool
    name: str
    vip: bool
    vip_ep: bool
    ids: Dict[str, MediaForeignIDType]

    joined_at: str = ""
    location: str = ""
    about: str = ""
    gender: str = ""
    age: int = 0
    images: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Comment(AbstractBaseModel):
    id: int
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    comment: str
    spoiler: bool
    review: bool
    replies: int
    likes: int
    user_rating: int
    user: User


@dataclass
class TraktList(AbstractBaseModel):
    name: str
    description: str
    privacy: str
    display_numbers: bool
    allow_comments: bool
    sort_by: str
    sort_how: str
    created_at: datetime
    updated_at: datetime
    item_count: int
    comment_count: int
    likes: int
    ids: Dict[str, MediaForeignIDType]


@dataclass
class Episode(AbstractBaseModel):
    season: int
    number: int
    title: str
    ids: Any = ""

    number_abs: int = 0
    overview: str = ""
    rating: int = 0
    votes: int = 0
    comment_count: int = 0
    first_aired: str = ""
    updated_at: str = ""
    available_translations: List[str] = field(default_factory=list)
    runtime: int = 0


@dataclass
class Movie(AbstractBaseModel):
    title: int
    year: int
    ids: Dict[str, MediaForeignIDType]

    tagline: str = ""
    overview: str = ""
    released: str = ""
    runtime: int = 0
    country: str = ""
    updated_at: str = ""
    trailer: str = ""
    homepage: str = ""
    rating: int = 0
    votes: int = 0
    comment_count: int = 0
    language: str = ""
    available_translations: List[str] = field(default_factory=list)
    genres: List[str] = field(default_factory=list)
    certification: str = ""


@dataclass
class Person(AbstractBaseModel):
    name: str
    ids: Dict[str, MediaForeignIDType]


@dataclass
class Rating(AbstractBaseModel):
    rating: float
    votes: int
    distribution: Dict[str, int]
