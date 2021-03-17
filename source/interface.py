from discord import Guild
from discord.ext.commands import Context
from typing import Optional


class SourceInterface:

    def deactivate_guild(self, guild: Guild):
        raise NotImplementedError

    def get_guild_guest_role(self, ctx: Context) -> str:
        raise NotImplementedError

    def get_guild_guest_role_id(self, ctx: Context) -> Optional[int]:
        raise NotImplementedError

    def register_guild(self, guild: Guild) -> bool:
        raise NotImplementedError

    def set_guild_guest_role_comp(self, ctx: Context, name: str, id: int):
        raise NotImplementedError

    def set_guild_guest_role_id(self, ctx: Context, id: int):
        raise NotImplementedError

    def set_guild_member_role_comp(self, ctx: Context, name: str, id: int):
        raise NotImplementedError
