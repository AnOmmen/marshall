from command.exception.command_error import CommandError


class UnrecognizedAliasError(CommandError):
    _unrecognized_alias = 'Unrecognized alias of {alias_name}.'

    def __init__(self, alias_name: str):
        super().__init__(self._unrecognized_alias.replace('{alias_name}', alias_name))
