from service.exception.service_error import ServiceError


class UnrecognizedFlagError(ServiceError):
    _unrecognized_flag = 'Unrecognized flag given: {flag_name}'

    def __init__(self, flag_name: str):
        super().__init__(self._unrecognized_flag.replace('{flag_name}', flag_name))
