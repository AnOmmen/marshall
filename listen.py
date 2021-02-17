import os

from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.guild import Guild
from discord.member import Member
from source.default import DefaultSource
from source.interface import SourceInterface

intents: Intents = Intents(guilds=True, messages=True)
bot = commands.Bot(command_prefix='.', intents=intents)
source: SourceInterface = DefaultSource()


@bot.command()
async def marshall(ctx):
    await ctx.send('meow')


@bot.command()
async def me(ctx: Context):
    await ctx.send(about_me(ctx))


@bot.event
async def on_guild_join(guild: Guild):
    source.register_guild(guild.id)


@bot.event
async def on_guild_remove(guild: Guild):
    source.deactivate_guild(guild.id)


def about_me(ctx: Context) -> str:
    if isinstance(ctx.author, Member):
        ret_str = 'Meowmber: '
        if ctx.author.nick is not None:
            ret_str += ctx.author.nick
        else:
            ret_str += ctx.author.name
    else:
        ret_str = 'Meowser: ' + ctx.author.name
    return ret_str


if __name__ == '__main__':
    bot.run(os.environ['BOT_TOKEN'])
