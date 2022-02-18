from dotenv import load_dotenv
import sys

import guild_config

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if "-g" not in opts:
    raise SystemExit(f"Usage: {sys.argv[0]} -g <guild_id>")

load_dotenv('.env')

guild_config.init(args[0])

import discordbot

discordbot.run()
