from os.path import isfile
import logging

from discord.ext import commands
import discord

import discordbot.discord_settings as sett
from .commands.manage_commands import ManageTargetsCommands
from .commands.watch_commands import WatchCommands
from .commands.subscribe_commands import SubscribeCommands
from .controllers import subscribe_controller as sc
from vigilante import fileutils
import vigilante

# Pycord logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=sett.PYCORD_LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Discordbot logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=sett.DISCORDBOT_LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# logging.disable(logging.DEBUG)

# bot = discord.Bot()
bot = discord.Bot(debug_guilds=sett.DEBUG_GUILD_IDS)


def create_subscriptions_file() -> None:
    fileutils.create_empty_json_file(sett.SUBSCRIPTIONS_FILE)
    fileutils.create_empty_key_in_file(sett.SUBSCRIPTIONS_FILE, 'targets')
    fileutils.create_empty_key_in_file(sett.SUBSCRIPTIONS_FILE, 'tokens')
    fileutils.create_empty_key_in_file(sett.SUBSCRIPTIONS_FILE, 'target_tokens')
    logger.info(f'Created file: {sett.SUBSCRIPTIONS_FILE}')


def subscriptions_file_exist() -> bool:
    return isfile(sett.SUBSCRIPTIONS_FILE)


def setup(_bot):
    _bot.add_cog(ManageTargetsCommands(_bot))
    _bot.add_cog(WatchCommands(_bot))
    _bot.add_cog(SubscribeCommands(_bot))
    if not subscriptions_file_exist():
        create_subscriptions_file()


def run():
    global bot
    setup(bot)
    bot.run(sett.TOKEN)


@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} is now connected to Discord!')
    vigilante.init()

    vigilante_channels_list = [
        channel for channel in bot.get_guild(sett.GUILD_ID).channels
        if 'vigilante' in channel.name
    ]
    for channel in vigilante_channels_list:
        await channel.send("I'm up and ready for my duty. Please invoke the `/watch` command.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        with ctx.typing():
            await ctx.send(error, ephemeral=True)
