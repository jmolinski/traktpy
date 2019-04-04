MOVIE1 = {
    "title": "Guardians of the Galaxy",
    "year": 2014,
    "ids": {
        "trakt": 28,
        "slug": "guardians-of-the-galaxy-2014",
        "imdb": "tt2015381",
        "tmdb": 118340,
    },
}

MOVIE2 = {
    "title": "Guardians of the Galaxy",
    "year": 2014,
    "ids": {
        "trakt": 28,
        "slug": "guardians-of-the-galaxy-2014",
        "imdb": "tt2015381",
        "tmdb": 118340,
    },
}

MOVIE_PREMIERES = [
    {"released": "2014-08-01", "movie": MOVIE1},
    {"released": "2014-08-01", "movie": MOVIE2},
]

MOVIES = [MOVIE1, MOVIE2]

TRENDING_MOVIES = [{"watchers": 21, "movie": MOVIE1}, {"watchers": 17, "movie": MOVIE2}]

PLAYED_MOVIES = [
    {
        "watcher_count": 66667,
        "play_count": 109736,
        "collected_count": 27584,
        "movie": MOVIE1,
    },
    {
        "watcher_count": 76254,
        "play_count": 104242,
        "collected_count": 31877,
        "movie": MOVIE2,
    },
]

ANTICIPATED_MOVIES = [
    {"list_count": 5362, "movie": MOVIE1},
    {"list_count": 4405, "movie": MOVIE2},
]

BOX_OFFICE = [
    {"revenue": 48464322, "movie": MOVIE1},
    {"revenue": 17728313, "movie": MOVIE2},
]

UPDATED_MOVIES = [{"updated_at": "2014-09-22T21:56:03.000Z", "movie": MOVIE1}]

EXTENDED_MOVIE = {
    "title": "TRON: Legacy",
    "year": 2010,
    "ids": {
        "trakt": 343,
        "slug": "tron-legacy-2010",
        "imdb": "tt1104001",
        "tmdb": 20526,
    },
    "tagline": "The Game Has Changed.",
    "overview": "Sam Flynn, the tech-savvy and daring son of Kevin Flynn, investigates his father's disappearance and is pulled into The Grid. With the help of  a mysterious program named Quorra, Sam quests to stop evil dictator Clu from crossing into the real world.",
    "released": "2010-12-16",
    "runtime": 125,
    "country": "us",
    "updated_at": "2014-07-23T03:21:46.000Z",
    "trailer": None,
    "homepage": "http://disney.go.com/tron/",
    "rating": 8,
    "votes": 111,
    "comment_count": 92,
    "language": "en",
    "available_translations": ["en"],
    "genres": ["action"],
    "certification": "PG-13",
}

ALIASES = [
    {"title": "Batman 1 - Batman Begins", "country": "ca"},
    {"title": "Batman 5 Begins", "country": "br"},
]

RELEASES = [
    {
        "country": "us",
        "certification": "PG",
        "release_date": "2010-12-16",
        "release_type": "theatrical",
        "note": None,
    },
    {
        "country": "gb",
        "certification": "PG",
        "release_date": "2010-12-17",
        "release_type": "theatrical",
        "note": None,
    },
]
