import os
from discord.ext import commands

bot = commands.Bot(command_prefix='.')


@bot.command()
async def marshall(ctx):
    await ctx.send('meow')

bot.run(os.environ['BOT_TOKEN'])
