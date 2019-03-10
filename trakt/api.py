from typing import Any


class TraktApi:
    authenticated: bool

    def __init__(self) -> None:
        self.authenticated = False

    def login(self) -> None:
        pass

    def run(self, path: str, *args: Any, **kwargs: Any) -> Any:
        pass
