from exception.marshall_error import MarshallError


class SourceError(MarshallError):

    def __init__(self, message):
        self.message = message
