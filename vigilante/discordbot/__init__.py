from discord.ext import commands
import discord

from discordbot.settings import TOKEN
from .commands.manage_commands import ManageTargetsCommands
from .commands.watch_commands import WatchCommands
from .commands.subscribe_commands import SubscribeCommands
from .controllers import subscribe_controller as sc
import vigilante

bot = discord.Bot()


def setup(_bot):
    _bot.add_cog(ManageTargetsCommands(_bot))
    _bot.add_cog(WatchCommands(_bot))
    _bot.add_cog(SubscribeCommands(_bot))
    if not sc.subscriptions_file_exist():
        sc.create_subscriptions_file()


def run():
    global bot
    setup(bot)
    bot.run(TOKEN)


@bot.event
async def on_ready():
    print(f'{bot.user.name} is now connected to Discord!')
    vigilante.init()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        with ctx.typing():
            await ctx.send(error, ephemeral=True)
