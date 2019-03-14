from __future__ import annotations

from typing import Any, Callable, Optional

from trakt.core.abstract import AbstractApi


class Validator:
    def _validate(
        self, *args: Any, **kwargs: Any
    ) -> Optional[bool]:  # pragma: no cover
        return True

    def validate(self, *args: Any, **kwargs: Any) -> bool:
        return self._validate(*args, **kwargs) is not False


class AuthRequiredValidator(Validator):
    def _validate(
        self, client: AbstractApi, *args: Any, **kwargs: Any
    ) -> Optional[bool]:
        if not client.authenticated:
            return False


class RequiredArgsValidator(Validator):
    def _validate(self, *args: Any, path: Any, **kwargs: Any) -> Optional[bool]:
        for p in path.req_args:
            arg_name = p[1:]
            if arg_name not in kwargs or kwargs[arg_name] in (None, [], {}):
                return False


class OptionalArgsValidator(Validator):
    """
    path: 'a/?b/?c'
    if c is provided then b must be provided
    """

    def _validate(self, *args: Any, path: Any, **kwargs: Any) -> Optional[bool]:
        require_previous = False

        for p in path.opt_args[::-1]:
            arg_name = p[1:]
            if require_previous:
                if arg_name not in kwargs or kwargs[arg_name] in (None, [], {}):
                    return False
            elif arg_name in kwargs:
                require_previous = True


class PerArgValidator(Validator):
    def __init__(self, arg_name: str, f: Callable[[Any], bool]) -> None:
        self.arg_name = arg_name
        self.boolean_check = f

    def _validate(self, *args: Any, **kwargs: Any) -> Optional[bool]:
        if self.arg_name in kwargs:
            return self.boolean_check(kwargs[self.arg_name])
