class ClientError(Exception):
    pass


class NotAuthenticated(ClientError):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
