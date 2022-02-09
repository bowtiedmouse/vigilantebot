import os

from dotenv import load_dotenv

import vigilante

load_dotenv()

GUILD_IDS = [int(guild) for guild in os.getenv('DISCORD_GUILD_IDS').split(',')]
ALLOWED_CHANNELS = [int(channel) for channel in os.getenv('DISCORD_ALLOWED_CHANNELS').split(',')]
ADMIN_ROLES = os.getenv('DISCORD_ALLOWED_ROLES').split(',')
WATCH_FREQUENCY_MINUTES = 10
TOKEN = os.getenv('DISCORD_TOKEN')

TARGETS_LIST = vigilante.get_targets_alias_list()
