import os

from dotenv import load_dotenv

from vigilante import get_targets_alias_list

load_dotenv()

GUILD_IDS = [int(guild) for guild in os.getenv('DISCORD_GUILD_IDS').split(',')]
ALLOWED_CHANNELS = [int(channel) for channel in os.getenv('DISCORD_ALLOWED_CHANNELS').split(',')]
ADMIN_ROLES = os.getenv('DISCORD_ALLOWED_ROLES').split(',')
WATCH_FREQUENCY_SECONDS = 4 * 60 + 55
TOKEN = os.getenv('DISCORD_TOKEN')

SUBSCRIPTIONS_FILE = 'data/subscriptions.json'
TARGETS_LIST = get_targets_alias_list()
