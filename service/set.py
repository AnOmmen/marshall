from context.execution import ExecutionContext
from data.flag import Flag
from discord import Role
from service.base import Service
from typing import List, Optional


class SetService(Service):
    _role_creation_reason = 'Requested by the .set command.'
    _role_not_found = 'Role by the name of "{role_name}" not found. If you would like meow to create the role, please' \
                      ' include the -c, --create, flag.'
    _role_set = '{role_name} set as {role_type} role.'

    async def _execute(self, ctx: ExecutionContext):

        for flag, params in ctx.flags.items():

            if flag.name == 'rg':

                role_name = params[0]
                role: Optional[Role] = ctx.get_guild_role(role_name)

                if role is None:

                    if ctx.has_flag('c'):
                        role = await ctx.create_guild_guest_role(role_name, self._role_creation_reason)

                    else:
                        await ctx.send(self._role_not_found.replace('{role_name}', role_name))
                        continue

                ctx.set_guild_guest_role_comp(role.name, role.id)
                await ctx.send(self._role_set.replace('{role_name}', role.name).replace('{role_type}', 'guest'))

            elif flag.name == 'rm':

                role_name = params[0]
                role: Optional[Role] = ctx.get_guild_role(role_name)

                if role is None:

                    if ctx.has_flag('c'):
                        role = await ctx.create_guild_member_role(role_name, self._role_creation_reason)

                    else:
                        await ctx.send(self._role_not_found.replace('{role_name}', role_name))
                        continue

                ctx.set_guild_member_role_comp(role.name, role.id)
                await ctx.send(self._role_set.replace('{role_name}', role.name).replace('{role_type}', 'member'))

    def _flags(self) -> List[Flag]:
        return [
            Flag('c', ['create'], 0),
            Flag('rg', ['guest-role', 'role-guest'], 1),
            Flag('rm', ['member-role', 'role-member'], 1)
        ]

    def _num_params(self) -> int:
        return 0
