from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from trakt.core.models import Episode, Season, Show


@dataclass
class TrendingShow:
    watchers: int
    show: Show


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
    production: List[ShowCrewCredit] = field(default_factory=list)
    art: List[ShowCrewCredit] = field(default_factory=list)
    crew: List[ShowCrewCredit] = field(default_factory=list)
    costume_make_up: List[ShowCrewCredit] = field(default_factory=list)
    directing: List[ShowCrewCredit] = field(default_factory=list)
    writing: List[ShowCrewCredit] = field(default_factory=list)
    sound: List[ShowCrewCredit] = field(default_factory=list)
    camera: List[ShowCrewCredit] = field(default_factory=list)


@dataclass
class ShowCredits:
    cast: List[ShowCastCredit]
    crew: ShowCrewCredits


@dataclass
class ShowWithStats:
    watcher_count: int
    play_count: int
    collected_count: int
    show: Show


@dataclass
class AnticipatedShow:
    list_count: int
    show: Show


@dataclass
class UpdatedShow:
    updated_at: datetime
    show: Show


@dataclass
class ShowTranslation:
    title: str
    overview: str
    language: str


@dataclass
class EpisodeCollectionProgress:
    number: int
    completed: bool
    collected_at: Optional[datetime] = None


@dataclass
class SeasonCollectionProgress:
    number: int
    aired: int
    completed: int
    episodes: List[EpisodeCollectionProgress]


@dataclass
class ShowCollectionProgress:
    aired: int
    completed: int
    last_collected_at: datetime
    seasons: List[SeasonCollectionProgress]
    hidden_seasons: List[Season]
    last_episode: Episode
    next_episode: Optional[Episode] = None


@dataclass
class EpisodeWatchedProgress:
    number: int
    completed: bool
    last_watched_at: Optional[datetime] = None


@dataclass
class SeasonWatchedProgress:
    number: int
    aired: int
    completed: int
    episodes: List[EpisodeWatchedProgress]


@dataclass
class ShowWatchedProgress:
    aired: int
    completed: int
    seasons: List[SeasonWatchedProgress]
    hidden_seasons: List[Season]
    last_episode: Optional[Episode] = None
    last_watched_at: Optional[datetime] = None
    next_episode: Optional[Episode] = None
    reset_at: Optional[datetime] = None


@dataclass
class ShowStats:
    watchers: int
    plays: int
    collectors: int
    collected_episodes: int
    comments: int
    lists: int
    votes: int
