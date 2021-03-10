from context.marshall_context import MarshallContext
from service.definition.access_level import AccessLevel
from source.interface import SourceInterface
from typing import Any, Dict, List
from utils.str_gen import StrGen


class ServiceInterface:
    _source: SourceInterface

    def __init__(self, source: SourceInterface):
        self._source = source

    async def _access_level(self) -> AccessLevel:
        return AccessLevel.ADMIN

    async def _execute(self, ctx: MarshallContext, arg_map: Dict[Any, List[str]]):
        raise NotImplementedError

    async def handle(self, ctx: MarshallContext, *args):

        if not await self._user_has_access(ctx):
            return

        flag = None
        values: List[str] = []
        arg_map: Dict[Any, List[str]] = {}

        for i in range(len(args[0])):
            if args[0][i].startswith('-'):
                if flag is not None:
                    arg_map[flag] = values
                    values = []
                flag = args[0][i][1:]
            else:
                values.append(args[0][i])

        if len(values) > 0:
            arg_map[0] = values

        await self._execute(ctx, arg_map)

    async def _user_has_access(self, ctx: MarshallContext) -> bool:

        access_level = await self._access_level()

        if access_level == AccessLevel.MEMBER:
            guest_role_id = self._source.get_guild_guest_role_id(ctx)
            for role in ctx.author.roles:
                if role.id == guest_role_id:
                    await ctx.send(StrGen.mistake_inj().capitalize() + "! " + ctx.command.name +
                                   " requires member or administrator access.")
                    return False

        elif access_level == AccessLevel.ADMIN:
            for role in ctx.author.roles:
                if role.permissions.administrator:
                    return True
            await ctx.send(StrGen.mistake_inj().capitalize() + "! " + ctx.command.name +
                           " requires administrator access.")
            return False

        return True
