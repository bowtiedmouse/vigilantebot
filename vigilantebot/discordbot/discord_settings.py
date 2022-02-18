import os

import guild_config

# from .env
# GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
# DEBUG_GUILD_IDS = [int(guild_id) for guild_id in os.getenv('DEBUG_GUILD_IDS')]
# # ALLOWED_CHANNELS = [int(channel) for channel in os.getenv('DISCORD_ALLOWED_CHANNELS').split(',')]
# ADMIN_ROLES = os.getenv('DISCORD_ALLOWED_ROLES').split(',')
# WATCH_FREQUENCY_SECONDS = 4 * 60 + 55
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG_GUILD_IDS = [int(guild_id) for guild_id in os.getenv('DEBUG_GUILD_IDS').split(',')]

# from config/<guild_id>.json
GUILD_ID = guild_config.get_guild_id()
# ALLOWED_CHANNELS = guild_config.get_allowed_channels()
# ADMIN_ROLES = guild_config.get_allowed_roles()
ADMIN_ROLES = os.getenv('ALLOWED_ROLES').split(',')

WATCH_FREQUENCY_SECONDS = 4 * 60 + 55

# GUILD_NAME = os.getenv('GUILD_NAME').replace(' ', '')
GUILD_NAME = guild_config.get_guild_name()
SUBSCRIPTIONS_FILE = f"data/subscriptions_{GUILD_NAME}.json"
PYCORD_LOG_FILE = f"logs/discord_{GUILD_NAME}.log"
DISCORDBOT_LOG_FILE = f"logs/discordbot_{GUILD_NAME}.log"
