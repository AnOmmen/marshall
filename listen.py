import os
from discord.ext import commands
from discord.member import Member

bot = commands.Bot(command_prefix='.')


@bot.command()
async def marshall(ctx):
    await ctx.send('meow')


@bot.command()
async def me(ctx):
    if isinstance(ctx.author, Member):
        await ctx.send('Meowmber: ' + ctx.author.nick)
    else:
        await ctx.send('Meowser: ' + ctx.author.name)


if __name__ == "__main__":
    bot.run(os.environ['BOT_TOKEN'])
