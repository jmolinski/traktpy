from typing import List, Optional


class ClientError(Exception):
    message: str = ""

    def __init__(
        self, message: Optional[str] = None, errors: Optional[List[Exception]] = None
    ) -> None:
        if not message:
            message = self.message

        super().__init__(message)
        if not errors:
            errors = []
        self.errors = errors


class NotAuthenticated(ClientError):
    message = "Not authenticated"


class ArgumentError(ClientError):
    message = "Argument error"
