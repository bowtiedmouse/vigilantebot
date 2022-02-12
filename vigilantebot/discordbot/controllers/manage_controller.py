# manage_controller.py
# Tasks for managing the watched targets list. Mostly admin-only. From the commands:
#   /add_target <target_alias> <target_address>
#   /remove_target <target_alias>
#   /list

from discordbot.discord_settings import TARGETS_LIST
from vigilante import get_addresses_from_alias


def get_targets_alias_list_with_addresses():
    targets_w_addresses = []
    for target_alias in TARGETS_LIST:
        addresses = get_addresses_from_alias(target_alias)
        targets_w_addresses.append(f"**{target_alias}** (*{', '.join(addresses)}*)")

    return targets_w_addresses
