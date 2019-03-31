from dataclasses import dataclass
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
    twitter: bool = False
    tumblr: bool = False
    medium: bool = False


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
class MovieWithStats:
    watcher_count: int
    player_count: int
    collected_count: int
    movie: Movie


@dataclass
class MovieStats:
    watchers: int
    plays: int
    collectors: int
    comments: int
    lists: int
    votes: int


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
    production: List[CrewMember]
    art: List[CrewMember]
    crew: List[CrewMember]
    costume_make_up: List[CrewMember]
    directing: List[CrewMember]
    writing: List[CrewMember]
    sound: List[CrewMember]
    camera: List[CrewMember]


@dataclass
class CastCrewList:
    cast: List[CastMember]
    crew: CrewList


@dataclass
class MovieRatings:
    rating: float
    votes: int
    distribution: Dict[str, int]


@dataclass
class MovieCastCredit:
    character: str
    movie: Movie


@dataclass
class MovieCrewCredit:
    job: str
    movie: Movie


@dataclass
class MovieCrewCredits:
    production: List[MovieCrewCredit]
    art: List[MovieCrewCredit]
    crew: List[MovieCrewCredit]
    costume_make_up: List[MovieCrewCredit]
    directing: List[MovieCrewCredit]
    writing: List[MovieCrewCredit]
    sound: List[MovieCrewCredit]
    camera: List[MovieCrewCredit]


@dataclass
class MovieCredits:
    cast: List[MovieCastCredit]
    crew: MovieCrewCredits


@dataclass
class ShowCastCredit:
    character: str
    show: Show


@dataclass
class ShowCrewCredit:
    job: str
    show: Show


@dataclass
class ShowCrewCredits:
    production: List[ShowCrewCredit]
    art: List[ShowCrewCredit]
    crew: List[ShowCrewCredit]
    costume_make_up: List[ShowCrewCredit]
    directing: List[ShowCrewCredit]
    writing: List[ShowCrewCredit]
    sound: List[ShowCrewCredit]
    camera: List[ShowCrewCredit]


@dataclass
class ShowCredits:
    cast: List[ShowCastCredit]
    crew: ShowCrewCredits


@dataclass
class Network:
    name: str


@dataclass
class CommentResponse(Comment):
    sharing: Sharing


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
    score: Optional[float]
    movie: Optional[Movie] = None
    list: Optional[TraktList] = None
    person: Optional[Person] = None
    episode: Optional[Episode] = None
    show: Optional[Show] = None


@dataclass
class MovieScrobble:
    id: int
    action: str
    progress: float
    sharing: Sharing
    movie: Movie


@dataclass
class EpisodeScrobble:
    id: int
    action: str
    progress: float
    sharing: Sharing
    episode: Episode
    show: Show
