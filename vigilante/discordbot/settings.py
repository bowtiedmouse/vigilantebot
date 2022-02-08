import os

from dotenv import load_dotenv

load_dotenv()

GUILD_IDS = [int(guild) for guild in os.getenv('DISCORD_GUILD_IDS').split(',')]
ALLOWED_CHANNELS = [int(channel) for channel in os.getenv('DISCORD_ALLOWED_CHANNELS').split(',')]
ALLOWED_ROLES = set.union(set(os.getenv('DISCORD_ALLOWED_ROLES').split(',')))
WATCH_FREQUENCY_MINUTES = 1
TOKEN = os.getenv('DISCORD_TOKEN')