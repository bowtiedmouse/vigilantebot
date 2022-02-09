from os.path import isfile
from typing import Union
import json
# import logging

from vigilante.settings import TARGET_ACCOUNTS_FILE
from vigilante.holdings import holdings_file_exists, create_holdings_file
from vigilante.target import Target
from vigilante.alerts import AlertLog as Log

# logger = logging.getLogger(__name__)

# list of Targets to watch
_targets = []


def _get_target_accounts_data() -> dict:
    assert isfile(TARGET_ACCOUNTS_FILE), "Need some accounts to watch!"

    try:
        with open(TARGET_ACCOUNTS_FILE, "r") as f:
            target_accounts_data = json.load(f)
        return target_accounts_data

    except json.decoder.JSONDecodeError as e:
        print(f"{TARGET_ACCOUNTS_FILE} file is malformed: {e}")


def get_address_from_alias(_alias: str) -> str:
    for _target in _targets:
        if _target.alias == _alias:
            return _target.addresses[0]
    return ''


def get_target_from_alias(_alias: str) -> Union[Target, None]:
    for _target in _targets:
        if _target.alias == _alias:
            return _target
    return None


def get_targets_alias_list() -> list[str]:
    return [_target['alias'] for _target in _get_target_accounts_data()]


def get_usd_balance_from_alias(alias: str) -> int:
    for _target in _targets:
        if _target.alias == alias:
            return _target.usd_balance
    return 0


def init() -> None:
    global _targets

    print("Initializing targets...")

    if not holdings_file_exists():
        create_holdings_file()

    _targets = [
        Target(user["alias"], user["addresses"])
        for user in _get_target_accounts_data()
    ]

    print("Targets ready.")


def watch_targets(report_empty: bool = False) -> list:
    global _targets
    if not len(_targets):
        init()

    print("Starting watch turn...")
    for _target in _targets:
        _target.watch()

    Log.sort()
    updates_str = Log.get_log_str(report_empty)
    print(updates_str)

    updates = Log.get_log()
    Log.clear()

    return updates


def watch_target(target_alias: str) -> list:
    _target = get_target_from_alias(target_alias)
    _target.watch()
    Log.sort()

    return Log.get_log()


def main():
    init()
    watch_targets(report_empty=True)


if __name__ == '__main__':
    main()
