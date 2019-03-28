from dataclasses import dataclass
from datetime import datetime
from typing import Any

from trakt.core.models import Episode, Movie, Show, TraktList, User


@dataclass
class EpisodePremiere:
    first_aired: str
    episode: Episode
    show: Show


@dataclass
class Country:
    name: str
    code: str


@dataclass
class TrendingShow:
    watchers: int
    show: Show


@dataclass
class TrendingMovie:
    watchers: int
    show: Movie


@dataclass
class Certification:
    name: str
    slug: str
    description: str


@dataclass
class Genre:
    name: str
    slug: str


@dataclass
class Language:
    name: str
    code: str


@dataclass
class ListResponse:
    like_count: int
    comment_count: int
    list: TraktList
    user: User


@dataclass
class MoviePremiere:
    released: str
    movie: Movie


@dataclass
class Sharing:
    twitter: bool
    tumblr: bool


@dataclass
class EpisodeCheckin:
    id: int
    watched_at: str
    sharing: Sharing
    episode: Episode
    show: Show


@dataclass
class MovieCheckin:
    id: int
    watched_at: str
    sharing: Sharing
    movie: Movie


@dataclass
class MovieStats:
    watcher_count: int
    player_count: int
    collected_count: int
    movie: Movie


@dataclass
class AnticipatedMovie:
    list_count: int
    movie: Movie


@dataclass
class BoxOffice:
    revenue: int
    movie: Movie


@dataclass
class UpdatedMovie:
    updated_at: datetime
    movie: Movie


@dataclass
class MovieAlias:
    title: str
    country: str


@dataclass
class MovieRelease:
    country: str
    certification: str
    release_date: datetime
    release_type: str
    note: Any


@dataclass
class MovieTranslation:
    title: str
    overview: str
    tagline: str
    language: str
