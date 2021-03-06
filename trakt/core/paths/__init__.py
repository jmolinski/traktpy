# flake8: noqa: F401
from trakt.core.paths.endpoint_mappings.calendars import CalendarsI
from trakt.core.paths.endpoint_mappings.checkin import CheckinI
from trakt.core.paths.endpoint_mappings.comments import CommentsI
from trakt.core.paths.endpoint_mappings.episodes import EpisodesI
from trakt.core.paths.endpoint_mappings.misc_mappings import (
    CertificationsI,
    CountriesI,
    GenresI,
    LanguagesI,
    ListsI,
    NetworksI,
    Path,
)
from trakt.core.paths.endpoint_mappings.movies import MoviesI
from trakt.core.paths.endpoint_mappings.people import PeopleI
from trakt.core.paths.endpoint_mappings.recommendations import RecommendationsI
from trakt.core.paths.endpoint_mappings.scrobble import ScrobbleI
from trakt.core.paths.endpoint_mappings.search import SearchI
from trakt.core.paths.endpoint_mappings.seasons import SeasonsI
from trakt.core.paths.endpoint_mappings.shows import ShowsI

DEFAULT_INTERFACES = {
    "countries": CountriesI,
    "calendars": CalendarsI,
    "shows": ShowsI,
    "genres": GenresI,
    "certifications": CertificationsI,
    "languages": LanguagesI,
    "lists": ListsI,
    "movies": MoviesI,
    "checkin": CheckinI,
    "people": PeopleI,
    "networks": NetworksI,
    "comments": CommentsI,
    "search": SearchI,
    "recommendations": RecommendationsI,
    "scrobble": ScrobbleI,
    "seasons": SeasonsI,
    "episodes": EpisodesI,
}
