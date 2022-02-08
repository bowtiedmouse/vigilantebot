from discord.ext import commands
import discord

from discordbot.settings import TOKEN
from .commands import manage
from .commands import watch


def setup(_bot):
    _bot.add_cog(manage.ManageTargetsCommands(_bot))
    _bot.add_cog(watch.WatchCommands(_bot))


def run():
    bot = discord.Bot()
    setup(bot)
    bot.run(TOKEN)

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            with ctx.typing():
                await ctx.send(error)
