import os

from discord import Permissions, Role
from discord.ext.commands import Context
from source.interface import SourceInterface


class ApplicationContext(Context):
    _source: SourceInterface

    def __init__(self, ctx: Context, source: SourceInterface):
        super().__init__(
            message=ctx.message,
            bot=ctx.bot,
            args=ctx.args,
            kwargs=ctx.kwargs,
            prefix=ctx.prefix,
            command=ctx.command,
            view=ctx.view,
            invoked_with=ctx.invoked_with,
            invoked_subcommand=ctx.invoked_subcommand,
            subcommand_passed=ctx.subcommand_passed,
            command_failed=ctx.command_failed)
        self._source = source

    def init_guild_guest_role(self) -> int:
        guild_guest_role = self._source.get_guild_guest_role(self)
        for role in self.guild.roles:
            if guild_guest_role.lower() == role.name.lower():
                self._source.set_guild_guest_role_id(self, role.id)
                return role.id

        guest_role: Role = self.guild.create_role(
            name=guild_guest_role,
            permissions=Permissions(os.environ['DEFAULT_GUEST_PERMISSIONS']),
            hoist=True,
            mentionable=True, reason="Guild lacking dedicated guest role.")

        return guest_role.id
