from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional

from trakt.core.models import Movie
from trakt.core.paths.response_structs.common import Sharing


@dataclass
class TrendingMovie:
    watchers: int
    movie: Movie


@dataclass
class MoviePremiere:
    released: date
    movie: Movie


@dataclass
class MovieCheckin:
    id: int
    watched_at: str
    sharing: Sharing
    movie: Movie


@dataclass
class MovieWithStats:
    watcher_count: int
    play_count: int
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
class MovieRelease:
    country: str
    certification: str
    release_date: date
    release_type: str
    note: Optional[str] = None


@dataclass
class MovieTranslation:
    title: str
    overview: str
    tagline: str
    language: str


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
    production: List[MovieCrewCredit] = field(default_factory=list)
    art: List[MovieCrewCredit] = field(default_factory=list)
    crew: List[MovieCrewCredit] = field(default_factory=list)
    costume_make_up: List[MovieCrewCredit] = field(default_factory=list)
    directing: List[MovieCrewCredit] = field(default_factory=list)
    writing: List[MovieCrewCredit] = field(default_factory=list)
    sound: List[MovieCrewCredit] = field(default_factory=list)
    camera: List[MovieCrewCredit] = field(default_factory=list)


@dataclass
class MovieCredits:
    cast: List[MovieCastCredit]
    crew: MovieCrewCredits


@dataclass
class MovieScrobble:
    id: int
    action: str
    progress: float
    sharing: Sharing
    movie: Movie
