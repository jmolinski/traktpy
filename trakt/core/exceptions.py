from typing import List, Optional


class ClientError(Exception):
    pass


class NotAuthenticated(ClientError):
    def __init__(self, message: str, errors: Optional[List[Exception]] = None) -> None:
        super().__init__(message)
        if not errors:
            errors = []
        self.errors = errors
