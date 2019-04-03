# traktpy
[![Build Status](https://travis-ci.org/jmolinski/traktpy.svg?branch=master)](https://travis-ci.org/jmolinski/traktpy)
[![Coverage Status](https://coveralls.io/repos/github/jmolinski/traktpy/badge.svg?branch=master)](https://coveralls.io/github/jmolinski/traktpy?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/56fa3c9b591a4bf96dfe/maintainability)](https://codeclimate.com/github/jmolinski/traktpy/maintainability)

Python library for accessing the Trakt.tv REST api.
---

The goal of this library is to provide the end user with a pythonic, easy to use interface while keeping it as close as possible to the original Trakt API design so that the official documentation can be used as a reference. 
Python3.7+ is required to run this library. 

All methods have detailed type annotations. That allows for precise code completion both for API calls and accessing response structs.

Library in development.

---

Sample usage
```python
from trakt import Trakt

client = Trakt(your_client_id, your_client_secret, oauth={'redirect_uri': 'your callback url'})

# redirect user to
redirect_url = client.oauth.get_redirect_url()

# use code from callback to sign user in
user = client.oauth.get_token(code=code)

```

```python
from trakt import Trakt

client = Trakt(your_client_id, your_client_secret)
client.set_user(SAVED_LOGGED_IN_USER)

for movie in client.movies.get_trending():
    print(movie.title)
    
    client.recommendations.hide_movie(movie=movie)
```

```python
from trakt import Trakt

client = Trakt(your_client_id, your_client_secret)
client.set_user(SAVED_LOGGED_IN_USER)

movie_slug = "monty-python-and-the-holy-grail-1975"
scrobble_status = client.scrobble.start_scrobble(movie=movie_slug, progress=15)

print(scrobble_status.movie.title)

```

---
Todo 0.1.0:
- http component retries
- possibly get rid of abstracts
- add missing interfaces tests
- docs
- pypi release

---
Todo 0.2.0:
- sync

- pagination: 
    - custom iter/generator: keep information about page count
    - pagination extras (limit exact items, per endpoint default limit, config)
- methods on models (episode.rate() etc)
- user profile
- caching (networks, countries etc)
