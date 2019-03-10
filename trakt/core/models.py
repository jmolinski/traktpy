from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import jsons


class _AbstractFromJson:
    pass


T = TypeVar("T", bound=_AbstractFromJson)
MediaForeignIDType = Type[Union[int, str, None]]


class AbstractBaseModel(_AbstractFromJson):
    @classmethod
    def from_json(cls: Type[T], data: Dict[str, Any]) -> T:
        obj = jsons.load(data, cls)
        return cast(T, obj)


@dataclass
class Show(AbstractBaseModel):
    title: str
    year: int
    ids: Dict[str, MediaForeignIDType]


@dataclass
class Certification(AbstractBaseModel):
    name: str
    slug: str
    description: str


@dataclass
class User(AbstractBaseModel):
    username: str
    private: bool
    name: str
    vip: bool
    vip_ep: bool
    ids: Dict[str, MediaForeignIDType]


@dataclass
class Comment(AbstractBaseModel):
    id: int
    parent_id: Optional[int]
    created_at: datetime
    comment: str
    spoiler: bool
    review: bool
    replies: int
    likes: int
    user_rating: int
    user: User


@dataclass
class Country(AbstractBaseModel):
    name: str
    code: str


@dataclass
class Genre(AbstractBaseModel):
    name: str
    slug: str


@dataclass
class Language(AbstractBaseModel):
    name: str
    code: str


@dataclass
class MediaList(AbstractBaseModel):
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
    ids: Dict[str, MediaForeignIDType]


@dataclass
class Movie(AbstractBaseModel):
    title: int
    year: int
    ids: Dict[str, MediaForeignIDType]


@dataclass
class MovieDetails(Movie):
    tagline: str
    overview: str
    released: date
    runtime: int
    country: str
    updated_at: datetime
    trailer: Optional[str]
    homepage: Optional[str]
    rating: int
    votes: int
    comment_count: int
    language: str
    available_translations: List[str]
    genres: List[str]
    certification: str


@dataclass
class MovieAlias(AbstractBaseModel):
    title: str
    country: str


@dataclass
class MovieRelease(AbstractBaseModel):
    country: str
    certification: str
    release_date: date
    release_type: str
    note: Optional[str]


@dataclass
class MovieTranslation(AbstractBaseModel):
    title: str
    overview: str
    tagline: str
    language: str


@dataclass
class Person(AbstractBaseModel):
    name: str
    ids: Dict[str, MediaForeignIDType]


@dataclass
class Rating(AbstractBaseModel):
    rating: float
    votes: int
    distribution: Dict[str, int]


@dataclass
class MovieStats(AbstractBaseModel):
    watchers: int
    plays: int
    collectors: int
    comments: int
    lists: int
    votes: int
