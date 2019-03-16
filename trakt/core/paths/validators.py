from __future__ import annotations

from typing import Any, Callable

from trakt.core.abstract import AbstractApi
from trakt.core.exceptions import ArgumentError, NotAuthenticated


class Validator:
    def validate(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        return None


class AuthRequiredValidator(Validator):
    def validate(self, client: AbstractApi, *args: Any, **kwargs: Any) -> None:
        if not client.authenticated:
            raise NotAuthenticated


class RequiredArgsValidator(Validator):
    def validate(self, *args: Any, path: Any, **kwargs: Any) -> None:  # type: ignore
        for p in path.req_args:
            arg_name = p[1:]
            if arg_name not in kwargs or kwargs[arg_name] in (None, [], {}):
                raise ArgumentError(f"missing required {arg_name} argument")


class OptionalArgsValidator(Validator):
    """
    path: 'a/?b/?c'
    if c is provided then b must be provided
    """

    def validate(self, *args: Any, path: Any, **kwargs: Any) -> None:  # type: ignore
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
