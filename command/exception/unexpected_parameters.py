from command.exception.command_error import CommandError
from typing import List


class UnexpectedParametersError(CommandError):
    _unexpected_parameters = 'Unexpected parameters'
    _for_flag = ' for {flag_name}:'

    def __init__(self, params: List[str], flag_name=None):
        message = self._unexpected_parameters
        message += self._for_flag.replace('{flag_name}', flag_name) if flag_name is not None else ':'
        for param in params:
            message += ' ' + param + ','
        message = message[:-1] + '.'
        super().__init__(message)
