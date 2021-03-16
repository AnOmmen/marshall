from service.exception.service_error import ServiceError


class UnrecognizedAliasError(ServiceError):
    _unrecognized_alias = 'Unrecognized alias of {alias_name}.'

    def __init__(self, alias_name: str):
        super().__init__(self._unrecognized_alias.replace('{alias_name}', alias_name))
