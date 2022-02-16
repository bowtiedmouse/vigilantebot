import json

_GUILD_CONFIG = {}


def init(guild_id: str):
    global _GUILD_CONFIG
    with open('config/' + guild_id + '.json') as config_file:
        _GUILD_CONFIG = json.load(config_file)


def get_guild_id() -> int:
    global _GUILD_CONFIG
    return int(_GUILD_CONFIG['guild_id'])


def get_guild_name() -> str:
    global _GUILD_CONFIG
    return _GUILD_CONFIG['guild_name'].replace(' ', '')


def get_allowed_channels() -> list:
    global _GUILD_CONFIG
    return _GUILD_CONFIG['allowed_channels']


def get_allowed_roles() -> list:
    global _GUILD_CONFIG
    return _GUILD_CONFIG['allowed_roles']


def get_excluded_chains() -> list:
    global _GUILD_CONFIG
    return _GUILD_CONFIG['excluded_chains']
