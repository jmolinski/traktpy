# flake8: noqa: F401

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from trakt.core.models import (
    Comment,
    Episode,
    Movie,
    Person,
    Season,
    Show,
    TraktList,
    User,
)
from trakt.core.paths.response_structs.movie_structs import (
    AnticipatedMovie,
    BoxOffice,
    MovieCastCredit,
    MovieCheckin,
    MovieCredits,
    MovieCrewCredit,
    MovieCrewCredits,
    MoviePremiere,
    MovieRelease,
    MovieScrobble,
    MovieStats,
    MovieTranslation,
    MovieWithStats,
    Sharing,
    TrendingMovie,
    UpdatedMovie,
)
from trakt.core.paths.response_structs.show_structs import (
    AnticipatedShow,
    ShowCollectionProgress,
    ShowCredits,
    ShowStats,
    ShowTranslation,
    ShowWatchedProgress,
    ShowWithStats,
    TrendingShow,
    UpdatedShow,
)


@dataclass
class EpisodePremiere:
    first_aired: datetime
    episode: Episode
    show: Show


@dataclass
class Country:
    name: str
    code: str


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
class EpisodeCheckin:
    id: int
    watched_at: str
    sharing: Sharing
    episode: Episode
    show: Show


@dataclass
class Alias:
    title: str
    country: str


@dataclass
class CastMember:
    character: str
    person: Person


@dataclass
class CrewMember:
    job: str
    person: Person


@dataclass
class CrewList:
    production: List[CrewMember] = field(default_factory=list)
    art: List[CrewMember] = field(default_factory=list)
    crew: List[CrewMember] = field(default_factory=list)
    costume_make_up: List[CrewMember] = field(default_factory=list)
    directing: List[CrewMember] = field(default_factory=list)
    writing: List[CrewMember] = field(default_factory=list)
    sound: List[CrewMember] = field(default_factory=list)
    camera: List[CrewMember] = field(default_factory=list)


@dataclass
class CastCrewList:
    cast: List[CastMember]
    crew: CrewList


@dataclass
class RatingsSummary:

    rating: float
    votes: int
    distribution: Dict[Any, Any]


@dataclass
class Network:
    name: str


@dataclass
class CommentResponse:
    id: int
    created_at: datetime
    comment: str
    spoiler: bool
    review: bool
    replies: int
    likes: int
    user: User
    parent_id: Optional[int] = None
    user_rating: Optional[int] = None
    updated_at: Optional[datetime] = None
    sharing: Optional[Sharing] = None


@dataclass
class CommentItemOnly:
    type: str
    list: Optional[TraktList] = None
    movie: Optional[Movie] = None
    episode: Optional[Episode] = None
    show: Optional[Show] = None
    season: Optional[Season] = None


@dataclass
class CommentAndItem:
    type: str
    comment: Comment
    list: Optional[TraktList] = None
    movie: Optional[Movie] = None
    episode: Optional[Episode] = None
    show: Optional[Show] = None
    season: Optional[Season] = None


@dataclass
class SearchResult:
    type: str
    score: Optional[float] = None
    movie: Optional[Movie] = None
    list: Optional[TraktList] = None
    person: Optional[Person] = None
    episode: Optional[Episode] = None
    show: Optional[Show] = None


@dataclass
class EpisodeScrobble:
    id: int
    action: str
    progress: float
    sharing: Sharing
    episode: Episode
    show: Show


@dataclass
class SeasonEpisodeStats:
    watchers: int
    plays: int
    collectors: int
    collected_episodes: int
    comments: int
    lists: int
    votes: int


@dataclass
class EpisodeTranslation:
    title: str
    overview: str
    language: str


@dataclass
class CommentLiker:
    liked_at: datetime
    user: User
