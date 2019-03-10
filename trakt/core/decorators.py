from typing import Any, Callable

from trakt.core.exceptions import NotAuthenticated


def auth_required(f: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(self, *args: Any, **kwargs: Any):
        if not self.authenticated:
            raise NotAuthenticated

        return f(self, *args, **kwargs)
    return wrapper
