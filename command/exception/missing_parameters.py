from command.exception.command_error import CommandError


class MissingParametersError(CommandError):
    _missing_parameters = 'Missing {num_params} parameter'
    _for_flag = ' for {flag_name}.'

    def __init__(self, num_params, flag_name=None):
        message = self._missing_parameters.replace('{num_params}', str(num_params))
        message += '' if num_params == 1 else 's'
        message += self._for_flag.replace('{flag_name}', flag_name) if flag_name is not None else '.'
        super().__init__(message)
