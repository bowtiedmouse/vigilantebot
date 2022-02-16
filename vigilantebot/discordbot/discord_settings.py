import os

from vigilante import get_targets_alias_list

GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
# ALLOWED_CHANNELS = [int(channel) for channel in os.getenv('DISCORD_ALLOWED_CHANNELS').split(',')]
ADMIN_ROLES = os.getenv('DISCORD_ALLOWED_ROLES').split(',')
WATCH_FREQUENCY_SECONDS = 4 * 60 + 55
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD_NAME = os.getenv('GUILD_NAME').replace(' ', '')
SUBSCRIPTIONS_FILE = f"data/subscriptions_{GUILD_NAME}.json"
PYCORD_LOG_FILE = f"logs/discord_{GUILD_NAME}.log"
DISCORDBOT_LOG_FILE = f"logs/discordbot_{GUILD_NAME}.log"

TARGETS_LIST = get_targets_alias_list()
