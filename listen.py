import os

from context.marshall_context import MarshallContext
from discord import Guild, Intents, Member, Role
from discord.ext.commands import Bot, Context
from discord.user import BaseUser
from service.interface import ServiceInterface
from service.set import SetService
from source.postgres import PostgresSource
from source.interface import SourceInterface

intents: Intents = Intents(guilds=True, members=True, messages=True)
bot = Bot(command_prefix='.', intents=intents)
source: SourceInterface = PostgresSource()
set_service: ServiceInterface = SetService(source)


@bot.command()
async def marshall(ctx: Context):
    await ctx.send('meow')


@bot.command()
async def me(ctx: Context):
    await ctx.send(about_me(ctx.author))


@bot.command()
async def role(ctx: Context, *, role_name: str):
    guild: Guild = ctx.guild
    await ctx.send("Exists" if has_role(guild.roles, role_name) else "Doesn't Exist")


@bot.command()
async def set(ctx: Context, *args):
    await set_service.handle(MarshallContext(ctx, source), args)


@bot.event
async def on_guild_join(guild: Guild):
    source.register_guild(guild)


@bot.event
async def on_guild_remove(guild: Guild):
    source.deactivate_guild(guild)


@bot.event
async def on_member_join(member: Member):
    pass


def about_me(user: BaseUser) -> str:
    return user.name + '#' + user.discriminator


def has_role(roles: [Role], role_name: str) -> bool:
    for role in roles:
        if role.name == role_name:
            return True


if __name__ == '__main__':
    bot.run(os.environ['BOT_TOKEN'])
