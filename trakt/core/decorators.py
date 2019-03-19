from typing import Any, Callable

from trakt.core.exceptions import NotAuthenticated


def auth_required(f: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not self.client.user:
            raise NotAuthenticated

        return f(self, *args, **kwargs)

    return wrapper
