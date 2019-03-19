from __future__ import annotations

from typing import Any, Callable

from trakt.core.abstract import AbstractApi
from trakt.core.exceptions import ArgumentError, NotAuthenticated


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
    def __init__(self, arg_name: str, f: Callable[[Any], bool]) -> None:
        self.arg_name = arg_name
        self.boolean_check = f

    def validate(self, *args: Any, **kwargs: Any) -> None:
        if self.arg_name in kwargs:
            if not self.boolean_check(kwargs[self.arg_name]):
                raise ArgumentError(
                    f"invalid {self.arg_name}={kwargs[self.arg_name]} argument value"
                )


class ExtendedValidator(Validator):
    def validate(self, *args: Any, path: Any, **kwargs: Any) -> None:
        if "extended" in kwargs:
            if kwargs["extended"] not in path.extended:
                message = f"invalid extended={kwargs['extended']} argument value; "

                if path.extended:
                    message += f"possible extended values: {path.extended}"
                else:
                    message += "this endpoint doesn't accept extended parameter"

                raise ArgumentError(message)


class FiltersValidator(Validator):
    def validate(self, *args: Any, path: Any, **kwargs: Any) -> None:
        pass
