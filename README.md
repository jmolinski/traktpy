# traktpy
[![Coverage Status](https://coveralls.io/repos/github/jmolinski/traktpy/badge.svg?branch=master)](https://coveralls.io/github/jmolinski/traktpy?branch=master)

Python library for accessing the Trakt.tv REST api.
---

The goal of this library is to provide the end user with a pythonic, easy to use interface while keeping it as close as possible to the original Trakt API design so that the official documentation can be used as a reference. 
Python3.7+ is required to run this library. 

All methods have detailed type annotations. That allows for precise code completion both for API calls and accessing response structs.

Library development is stalled. You may use https://trakt.docs.apiary.io/ as a reference.

---

# Sample usage

OAuth
```python
from trakt import Trakt

client = Trakt(your_client_id, your_client_secret, oauth={'redirect_uri': 'your callback url'})

# redirect user to
redirect_url = client.oauth.get_redirect_url()

# use code from callback to sign user in
user = client.oauth.get_token(code=code)

```

Movies, recommendations
```python
from trakt import Trakt

client = Trakt(your_client_id, your_client_secret)
client.set_user(SAVED_LOGGED_IN_USER)

for movie in client.movies.get_trending():
    print(movie.title)
    
    client.recommendations.hide_movie(movie=movie)
```

Scrobble
```python
from trakt import Trakt

client = Trakt(your_client_id, your_client_secret)
client.set_user(SAVED_LOGGED_IN_USER)

movie_slug = "monty-python-and-the-holy-grail-1975"
scrobble_status = client.scrobble.start_scrobble(movie=movie_slug, progress=15)

print(scrobble_status.movie.title)

```

---

# Exceptions
The library performs basic argument validation before making the request. 
You can expect a meaningful error message if there is an obvious problem - trying to access authorized-only endpoint without authorization, invalid argument format, missing required arguments, passing an invalid argument value.

All custom exceptions inherit from `trakt.core.exceptions.TraktError`.

All argument-related validations will raise exceptions inheriting from `trakt.core.exceptions.ArgumentError`.

Authorization errors (user not authenticated) will raise `trakt.core.exceptions.NotAuthenticated`.

Request related errors (4xx-5xx) will raise exceptions inheriting from `trakt.core.exceptions.RequestRelatedError`.
The exception will have a `code` field: `e.code`.

If the response is corrupt (can't be parsed) the parser will raise `trakt.core.exceptions.TraktResponseError`.

---
Todo 0.1.0:
- sync module
- user profile
- http component retries
- pypi release
