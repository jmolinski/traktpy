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
    ids: Dict[str, MediaForeignIDType]

    overview: Optional[str] = None
    first_aired: Optional[datetime] = None
    airs: Optional[Dict[str, Any]] = None
    runtime: Optional[int] = None
    certification: Optional[str] = None
    network: Optional[str] = None
    country: Optional[str] = None
    trailer: Optional[str] = None
    homepage: Optional[str] = None
    status: Optional[str] = None
    rating: Optional[int] = None
    votes: Optional[int] = None
    comment_count: Optional[int] = None
    updated_at: Optional[datetime] = None
    language: Optional[str] = None
    available_translations: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    aired_episodes: Optional[int] = None


@dataclass
class User(AbstractBaseModel):
    username: str
    private: bool
    name: str
    vip: bool
    vip_ep: bool
    ids: Dict[str, MediaForeignIDType]

    joined_at: Optional[datetime] = None
    location: Optional[str] = None
    about: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    images: Optional[Dict[str, Any]] = None


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
    user: Optional[User] = None


@dataclass
class Episode(AbstractBaseModel):
    season: int
    number: int
    title: str
    ids: Dict[str, MediaForeignIDType] = field(default_factory=dict)

    number_abs: Optional[int] = None
    overview: Optional[str] = None
    rating: Optional[int] = None
    votes: Optional[int] = None
    comment_count: Optional[int] = None
    first_aired: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    available_translations: Optional[List[str]] = None
    runtime: Optional[int] = None


@dataclass
class Movie(AbstractBaseModel):
    title: int
    year: int
    ids: Dict[str, MediaForeignIDType]

    tagline: Optional[str] = None
    overview: Optional[str] = None
    released: Optional[datetime] = None
    runtime: Optional[int] = None
    country: Optional[str] = None
    updated_at: Optional[datetime] = None
    trailer: Optional[str] = None
    homepage: Optional[str] = None
    rating: Optional[int] = None
    votes: Optional[int] = None
    comment_count: Optional[int] = None
    language: Optional[str] = None
    available_translations: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    certification: Optional[str] = None


@dataclass
class Person(AbstractBaseModel):
    name: str
    ids: Dict[str, MediaForeignIDType]

    biography: Optional[str] = None
    birthday: Optional[datetime] = None
    death: Optional[datetime] = None
    birthplace: Optional[str] = None
    homepage: Optional[str] = None


@dataclass
class Season(AbstractBaseModel):
    ids: Dict[str, MediaForeignIDType]


@dataclass
class Comment:
    id: int
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    comment: str
    spoiler: bool
    review: bool
    replies: int
    likes: int
    user_rating: Optional[int]
    user: User
