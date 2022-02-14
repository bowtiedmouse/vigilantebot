from os.path import isfile
import logging

from discord.ext import commands
import discord

from discordbot.discord_settings import TOKEN, SUBSCRIPTIONS_FILE, DEBUG_GUILD_IDS
from .commands.manage_commands import ManageTargetsCommands
from .commands.watch_commands import WatchCommands
from .commands.subscribe_commands import SubscribeCommands
from .controllers import subscribe_controller as sc
from vigilante import fileutils
import vigilante

# Pycord logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discordbot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# logging.disable(logging.DEBUG)

bot = discord.Bot(debug_guilds=DEBUG_GUILD_IDS)


def create_subscriptions_file() -> None:
    fileutils.create_empty_json_file(SUBSCRIPTIONS_FILE)
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'targets')
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'tokens')
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'target_tokens')
    print(f'Created file: {SUBSCRIPTIONS_FILE}')


def subscriptions_file_exist() -> bool:
    return isfile(SUBSCRIPTIONS_FILE)


def setup(_bot):
    _bot.add_cog(ManageTargetsCommands(_bot))
    _bot.add_cog(WatchCommands(_bot))
    _bot.add_cog(SubscribeCommands(_bot))
    if not subscriptions_file_exist():
        create_subscriptions_file()


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
