import os

from dotenv import load_dotenv
import sys
import logging

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if "-g" not in opts:
    raise SystemExit(f"Usage: {sys.argv[0]} -g <guild_id>")

load_dotenv('.env')
load_dotenv('.env_' + str(args[0]))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=DISCORDBOT_LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# logging.disable(logging.DEBUG)

logger.info(f"Connecting to {os.getenv('GUILD_NAME')} guild ({os.getenv('DISCORD_GUILD_ID')})")

import discordbot

discordbot.run()
