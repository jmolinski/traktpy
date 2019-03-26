from __future__ import annotations

from typing import Any, List, Optional


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


class RequestRelatedError(ClientError):
    status_code: Optional[int]
    response: Any

    def __init__(
        self, code: int = None, response=None, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)

        self.status_code = code
        self.response = response


class BadRequest(RequestRelatedError):
    status_code = 400


class Unauthorized(RequestRelatedError):
    status_code = 401


class Forbidden(RequestRelatedError):
    status_code = 403


class NotFound(RequestRelatedError):
    status_code = 404


class MethodNotFound(RequestRelatedError):
    status_code = 405


class Conflict(RequestRelatedError):
    status_code = 409


class PreconditionFailed(RequestRelatedError):
    status_code = 412


class UnprocessableEntity(RequestRelatedError):
    status_code = 422


class RateLimitExceeded(RequestRelatedError):
    status_code = 429


class ServerError(RequestRelatedError):
    status_code = 500


class ServiceUnavailable(RequestRelatedError):
    status_code = 503


class TraktResponseError(ClientError):
    message = "Response parsing error. Check response json structure."


class TraktTimeoutError(RequestRelatedError):
    message = "Pool timed out"
