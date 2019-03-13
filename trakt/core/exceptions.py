from typing import List, Optional


class ClientError(Exception):
    def __init__(self, message: str, errors: Optional[List[Exception]] = None) -> None:
        super().__init__(message)
        if not errors:
            errors = []
        self.errors = errors


class NotAuthenticated(ClientError):
    ...
