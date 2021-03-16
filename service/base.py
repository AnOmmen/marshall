from collections import OrderedDict
from context.execution import ExecutionContext
from context.application import ApplicationContext
from data.flag import Flag
from service.definition.access_level import AccessLevel
from service.exception.missing_parameters import MissingParametersError
from service.exception.unexpected_parameters import UnexpectedParametersError
from service.exception.unrecognized_alias import UnrecognizedAliasError
from service.exception.unrecognized_flag import UnrecognizedFlagError
from service.exception.service_error import ServiceError
from source.interface import SourceInterface
from typing import Dict, List, Union
from utils.str_gen import StrGen


class Service:
    _alias_map: Dict[str, str]
    _flag_map: Dict[str, Flag]
    _source: SourceInterface

    def __init__(self, source: SourceInterface):
        self._source = source
        self._alias_map = {}
        self._flag_map = {}
        for flag in self._flags():
            self._flag_map[flag.name] = flag
            for alias in flag.aliases:
                self._alias_map[alias] = flag.name

    async def __user_has_access(self, ctx: ApplicationContext) -> bool:

        access_level = self._access_level()

        if access_level == AccessLevel.MEMBER:
            guest_role_id = self._source.get_guild_guest_role_id(ctx)
            for role in ctx.author.roles:
                if role.id == guest_role_id:
                    await ctx.send(StrGen.mistake_inj().capitalize() + "! " + ctx.command.name +
                                   ' requires member or administrator access.')
                    return False

        elif access_level == AccessLevel.ADMIN:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send(StrGen.mistake_inj().capitalize() + '! ' + ctx.command.name +
                               ' requires administrator access.')
                return False

        return True

    def _access_level(self) -> AccessLevel:
        return AccessLevel.ADMIN

    async def _execute(self, ctx: ExecutionContext):
        raise NotImplementedError

    def _flags(self) -> List[Flag]:
        return []

    def _num_params(self) -> int:
        return -1

    async def handle(self, ctx: ApplicationContext, *args):

        if not await self.__user_has_access(ctx):
            return

        try:

            flagged_args = OrderedDict()
            flag_params: List[str] = []
            service_params: List[str] = []
            current_flag: Union[Flag, None] = None
            for arg in args[0]:

                # Check for flag (-) or alias (--) and only treat it as such if it has following characters
                if arg[0] == '-' and len(arg) > 1 and arg[1] != '-' or arg[:2] == '--' and len(arg) > 2:

                    flag_name: Union[None, str] = None

                    # Check if argument is an alias (--)
                    if arg[1] == '-':

                        # Check if the alias is recognized
                        if arg[2:] in self._alias_map.keys():
                            flag_name = self._alias_map[arg[2:]]

                    # Check if flag exists in map
                    elif arg[1:] in self._flag_map.keys():
                        flag_name = arg[1:]

                    # Check if a matching flag was found
                    if flag_name is not None:

                        # Check if a flag is currently being tracked
                        if current_flag is not None:

                            # Raise an error if the expected number of flag parameters are not present
                            if current_flag.num_params != -1 and len(flag_params) < current_flag.num_params:
                                raise MissingParametersError(
                                    current_flag.num_params - len(flag_params),
                                    current_flag.name)

                            # Currently tracked flag to the list of flagged arguments
                            flagged_args[current_flag] = flag_params
                            flag_params = []

                        # Set current flag to matched flag
                        current_flag = self._flag_map[flag_name]

                    # Raise an unrecognized error if the flag was not found
                    else:

                        if arg[1] == '-':
                            raise UnrecognizedAliasError(arg[2:])
                        else:
                            raise UnrecognizedFlagError(arg[1:])

                # Otherwise process argument as a parameter
                else:

                    # Check if there is a flag being tracked that requires additional parameters
                    if current_flag is not None and \
                            (current_flag.num_params == -1 or len(flag_params) < current_flag.num_params):
                        flag_params.append(arg)

                    # Otherwise add the parameter to the service parameter list
                    else:

                        # Check if the service is still expecting parameters, otherwise raise an error
                        if self._num_params() == -1 or len(service_params) < self._num_params():
                            service_params.append(arg)
                        else:
                            raise UnexpectedParametersError([arg])

            # Check there is a remaining flag being tracked
            if current_flag is not None:

                # Raise an error if the expected number of flag parameters are not present
                if current_flag.num_params != -1 and len(flag_params) < current_flag.num_params:
                    raise MissingParametersError(current_flag.num_params - len(flag_params), current_flag.name)

                flagged_args[current_flag] = flag_params

            # Raise an error if the expected number of service parameters are not present
            if self._num_params() != -1 and len(service_params) < self._num_params():
                raise MissingParametersError(self._num_params() - len(service_params))

            await self._execute(ExecutionContext(ctx, flagged_args, service_params))

        except ServiceError as error:
            await ctx.send(error.message)
