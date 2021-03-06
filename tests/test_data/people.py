from tests.test_data.movies import MOVIE1
from tests.test_data.shows import SHOW

PERSON = {
    "name": "Bryan Cranston",
    "ids": {"trakt": 1, "slug": "bryan-cranston", "imdb": "nm0186505", "tmdb": 17419},
    "biography": "Bryan Lee Cranston (born March 7, 1956) is an American actor, voice actor, writer and director.He is perhaps best known for his roles as Hal, the father in the Fox situation comedy \"Malcolm in the Middle\", and as Walter White in the AMC drama series Breaking Bad, for which he has won three consecutive Outstanding Lead Actor in a Drama Series Emmy Awards. Other notable roles include Dr. Tim Whatley on Seinfeld, Doug Heffernan's neighbor in The King of Queens, Astronaut Buzz Aldrin in From the Earth to the Moon, and Ted Mosby's boss on How I Met Your Mother.  Description above from the Wikipedia article Bryan Cranston, licensed under CC-BY-SA, full list of contributors on Wikipedia.",
    "birthday": "1956-03-07",
    "death": None,
    "birthplace": "San Fernando Valley, California, USA",
    "homepage": "http://www.bryancranston.com/",
}

MINI_PERSON = {
    "name": "Bryan Cranston",
    "ids": {"trakt": 1, "slug": "bryan-cranston", "imdb": "nm0186505", "tmdb": 17419},
}

MOVIE_CREDITS = {
    "cast": [{"character": "Joe Brody", "movie": MOVIE1}],
    "crew": {
        "directing": [{"job": "Director", "movie": MOVIE1}],
        "writing": [{"job": "Screenplay", "movie": MOVIE1}],
        "producing": [],
    },
}

SHOW_CREDITS = {
    "cast": [{"character": "Walter White", "show": SHOW}],
    "crew": {"production": [{"job": "Producer", "show": SHOW}]},
}

MOVIE_ALL_PEOPLE = {
    "cast": [
        {"character": "Sam Flynn", "person": MINI_PERSON},
        {"character": "Kevin Flynn / Clu", "person": MINI_PERSON},
    ],
    "crew": {
        "production": [{"job": "Casting", "person": MINI_PERSON}],
        "crew": [{"job": "Supervising Art Director", "person": MINI_PERSON}],
        "costume & make-up": [{"job": "Costume Design", "person": MINI_PERSON}],
        "directing": [{"job": "Director", "person": MINI_PERSON}],
        "writing": [{"job": "Screenplay", "person": MINI_PERSON}],
    },
}
