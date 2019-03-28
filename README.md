# traktpy
[![Build Status](https://travis-ci.org/jmolinski/traktpy.svg?branch=master)](https://travis-ci.org/jmolinski/traktpy)
[![Coverage Status](https://coveralls.io/repos/github/jmolinski/traktpy/badge.svg?branch=master)](https://coveralls.io/github/jmolinski/traktpy?branch=master)

Python library for accessing the Trakt.tv REST api.
---

The goal of this library is to provide the end user with a pythonic, easy to use interface while keeping it as close as possible to the original Trakt API design so that the official documentation can be used as a reference. 
Python3.7+ is required to run this library. 

All methods have detailed type annotations. That allows for precise code completion both for API calls and accessing response structs.

---
Todo:
- sync
- methods on models (episode.rate() etc)
- http component retries etc
- define all paths & user friendly aliases
- user profile
- possibly get rid of abstracts
- pagination extras (limit exact items, per endpoint default limit?, config)
- docs
- pypi release