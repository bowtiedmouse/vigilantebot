# manage_controller.py
# Tasks for managing the watched targets list. Mostly admin-only. From the commands:
#   /add_target <target_alias> <target_address>
#   /remove_target <target_alias>
#   /list

import vigilante


def get_targets_alias_list():
    return vigilante.get_targets_alias_list()
