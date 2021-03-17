import os

from discord import Permissions, Role
from discord.ext.commands import Context
from source.interface import SourceInterface
from typing import Optional


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

    async def create_guild_guest_role(self, name: str, reason: str) -> Role:
        return await self.guild.create_role(
            name=name,
            permissions=Permissions(int(os.environ['DEFAULT_GUEST_PERMISSIONS'])),
            hoist=True,
            mentionable=True,
            reason=reason)

    async def create_guild_member_role(self, name: str, reason: str) -> Role:
        return await self.guild.create_role(
            name=name,
            permissions=Permissions(int(os.environ['DEFAULT_MEMBER_PERMISSIONS'])),
            hoist=True,
            mentionable=True,
            reason=reason)

    def get_guild_guest_role(self) -> str:
        return self._source.get_guild_guest_role(self)

    async def get_guild_guest_role_id(self) -> Optional[int]:
        guest_role_id: Optional[int] = self._source.get_guild_guest_role_id(self)
        if guest_role_id is None:
            return await self.init_guild_guest_role()
        guest_role: Optional[Role] = self.guild.get_role(guest_role_id)
        if guest_role is None:
            return await self.init_guild_guest_role()
        return guest_role_id

    def get_guild_role(self, name: str) -> Optional[Role]:
        for role in self.guild.roles:
            if name.lower() == role.name.lower():
                return role
        return None

    async def init_guild_guest_role(self) -> int:
        guild_guest_role = self.get_guild_guest_role()
        guest_role: Optional[Role] = self.get_guild_role(guild_guest_role)

        if guest_role is not None:
            self.set_guild_guest_role_id(guest_role.id)
            return guest_role.id

        guest_role = await self.create_guild_guest_role(guild_guest_role, 'Guild lacking dedicated guest role.')
        return guest_role.id

    def set_guild_guest_role_comp(self, name: str, id: int):
        self._source.set_guild_guest_role_comp(self, name, id)

    def set_guild_guest_role_id(self, id: int):
        self._source.set_guild_guest_role_id(self, id)

    def set_guild_member_role_comp(self, name: str, id: int):
        self._source.set_guild_member_role_comp(self, name, id)
