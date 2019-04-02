# traktpy
[![Build Status](https://travis-ci.org/jmolinski/traktpy.svg?branch=master)](https://travis-ci.org/jmolinski/traktpy)
[![Coverage Status](https://coveralls.io/repos/github/jmolinski/traktpy/badge.svg?branch=master)](https://coveralls.io/github/jmolinski/traktpy?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/56fa3c9b591a4bf96dfe/maintainability)](https://codeclimate.com/github/jmolinski/traktpy/maintainability)

Python library for accessing the Trakt.tv REST api.
---

The goal of this library is to provide the end user with a pythonic, easy to use interface while keeping it as close as possible to the original Trakt API design so that the official documentation can be used as a reference. 
Python3.7+ is required to run this library. 

All methods have detailed type annotations. That allows for precise code completion both for API calls and accessing response structs.

---
Todo 0.1.0:
- http component retries etc
- possibly get rid of abstracts
- pagination extras (limit exact items, per endpoint default limit?, config)
- docs
- tests for interfaces
- pypi release

---
Todo 0.2.0:
- sync
- custom iter/generator: keep information about page count
- methods on models (episode.rate() etc)
- user profile
- caching (networks, countries etc)
