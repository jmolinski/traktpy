from __future__ import annotations

import re
from typing import Any, Callable, Dict, List

from trakt.core.abstract import AbstractApi
from trakt.core.exceptions import ArgumentError, NotAuthenticated

SINGLE_FILTERS = {"query", "years", "runtimes", "ratings"}
MULTI_FILTERS = {
    "genres",
    "languages",
    "countries",
    "certifications",
    "networks",
    "status",
}
MOVIE_FILTERS = {"certifications"}
SHOWS_FILTERS = {"certifications", "networks", "status"}


COMMON_FILTERS = SINGLE_FILTERS | {"genres", "languages", "countries"}

ALL_FILTERS = SINGLE_FILTERS | MULTI_FILTERS

STATUS_FILTER_VALUES = {
    "returning series",
    "in production",
    "planned",
    "canceled",
    "ended",
}


class Validator:
    def validate(
        self, *args: Any, client: AbstractApi, path: Any, **kwargs: Any
    ) -> None:  # pragma: no cover
        return None


class AuthRequiredValidator(Validator):
    def validate(self, *args: Any, client: AbstractApi, **kwargs: Any) -> None:
        if not client.user:
            raise NotAuthenticated


class RequiredArgsValidator(Validator):
    def validate(self, *args: Any, path: Any, **kwargs: Any) -> None:
        for p in path.req_args:
            arg_name = p[1:]
            if arg_name not in kwargs or kwargs[arg_name] in (None, [], {}):
                raise ArgumentError(f"missing required {arg_name} argument")


class OptionalArgsValidator(Validator):
    """
    path: 'a/?b/?c'
    if c is provided then b must be provided
    """

    def validate(self, *args: Any, path: Any, **kwargs: Any) -> None:
        require_previous = False

        for p in path.opt_args[::-1]:
            arg_name = p[1:]
            if require_previous:
                if arg_name not in kwargs or kwargs[arg_name] in (None, [], {}):
                    raise ArgumentError(f"missing {arg_name} argument")
            elif arg_name in kwargs:
                require_previous = True


class PerArgValidator(Validator):
    def __init__(self, arg_name: str, f: Callable[[Any], Any]) -> None:
        self.arg_name = arg_name
        self.boolean_check = f

    def validate(self, *args: Any, **kwargs: Any) -> None:
        if self.arg_name in kwargs:
            if not bool(self.boolean_check(kwargs[self.arg_name])):
                raise ArgumentError(
                    f"invalid {self.arg_name}={kwargs[self.arg_name]} argument value"
                )


class ExtendedValidator(Validator):
    def validate(self, *args: Any, path: Any, **kwargs: Any) -> None:
        if "extended" in kwargs:
            if len(path.extended) == 1 and kwargs["extended"] is True:
                return  # True = enabled, to be substituted later

            if kwargs["extended"] and kwargs["extended"] not in path.extended:
                message = f"invalid extended={kwargs['extended']} argument value; "

                if path.extended:
                    message += f"possible extended values: {path.extended}"
                else:
                    message += "this endpoint doesn't accept extended parameter"

                raise ArgumentError(message)


class FiltersValidator(Validator):
    filter_value_validators: Dict[str, Callable[[Any], bool]]

    def __init__(self):
        self.filter_value_validators = {
            "query": lambda s: isinstance(s, str) and s,
            "years": self.years_filter_validator,
            "genres": lambda g: isinstance(g, str) and g,
            "languages": lambda l: isinstance(l, str) and len(l) == 2,
            "countries": lambda c: isinstance(c, str) and len(c) == 2,
            "runtimes": lambda r: isinstance(r, (int, str)) and int(r) in range(1000),
            "ratings": self.ratings_filter_validator,
            "certifications": lambda c: isinstance(c, str) and c,
            "networks": lambda n: isinstance(n, str) and n,
            "status": lambda s: s in STATUS_FILTER_VALUES,
        }

    def validate(self, *args: Any, path: Any, **kwargs: Any) -> None:
        for k in kwargs:
            if k in ALL_FILTERS:
                self._validate_filter_arg(path.filters, k, kwargs[k])

    def _validate_filter_arg(
        self, allowed_filters: List[str], filter: str, value: Any
    ) -> None:
        if filter not in allowed_filters:
            raise ArgumentError(f"this endpoint doesnt accept {filter} filter")

        if filter in SINGLE_FILTERS and not isinstance(value, (int, str)):
            raise ArgumentError(f"{filter} filter only accepts 1 value")

        if filter in MULTI_FILTERS:
            self._validate_multi_filter(filter, value)

        self._validate_filter_value(filter, value)

    def _validate_multi_filter(self, filter: str, value: Any):
        if not isinstance(value, (tuple, list, str)):
            raise ArgumentError(
                f"{filter} filter invalid value (must be str or itarable of str)"
            )
        if isinstance(value, (list, tuple)):
            for v in value:
                if not isinstance(v, str):
                    raise ArgumentError(
                        f"{filter} filter invalid value (must be str or itarable of str)"
                    )

    def _validate_filter_value(self, filter: str, value: Any):
        if not isinstance(value, (list, tuple)):
            value = [value]
        for v in value:
            if not self.filter_value_validators[filter](v):
                raise ArgumentError(f"{filter}: {v} is not a valid value")

    @staticmethod
    def years_filter_validator(years: Any):
        years = [years] if isinstance(years, int) else years.split("-")

        if len(years) not in {1, 2}:
            return False

        for y in years:
            try:
                if int(y) not in range(1800, 2100):
                    return False
            except ValueError:
                return False

        return True

    @staticmethod
    def ratings_filter_validator(ratings: Any):
        return isinstance(ratings, str) and re.match(r"\d{1,2}-\d{1,3}", ratings)
