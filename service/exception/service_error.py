from exception.marshall_error import MarshallError


class ServiceError(MarshallError):

    def __init__(self, message):
        super().__init__(message)
