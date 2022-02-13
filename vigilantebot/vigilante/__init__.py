from os.path import isfile
from typing import Union
import json
import logging

from vigilante.settings import TARGET_ACCOUNTS_FILE
from vigilante.holdings import holdings_file_exists, create_holdings_file
from vigilante.target import Target
from vigilante.alerts import get_alert_log, get_alert_log_str, clear_alert_log, sort_alert_log


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/vigilante.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# logging.disable(logging.DEBUG)

# list of Targets to watch
_targets = []


def _get_target_accounts_data() -> dict:
    assert isfile(TARGET_ACCOUNTS_FILE), "No target accounts found. Need some accounts to watch!"

    try:
        with open(TARGET_ACCOUNTS_FILE, "r") as f:
            target_accounts_data = json.load(f)
        return target_accounts_data

    except json.decoder.JSONDecodeError as e:
        print(f"{TARGET_ACCOUNTS_FILE} file is malformed: {e}")


def get_addresses_from_alias(_alias: str) -> list:
    for _target in _targets:
        if _target.alias == _alias:
            return _target.addresses
    return []


def get_target_from_alias(_alias: str) -> Union[Target, None]:
    for _target in _targets:
        if _target.alias == _alias:
            return _target
    return None


def get_targets_alias_list() -> list[str]:
    return [_target['alias'] for _target in _get_target_accounts_data().values()]


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
        for user in _get_target_accounts_data().values()
    ]

    print("Targets ready.")


def watch_targets(report_empty: bool = False) -> list:
    global _targets
    if not len(_targets):
        logger.warning('Targets are not initialized.')
        raise

    print("Starting watch turn...")
    for _target in _targets:
        _target.watch()

    sort_alert_log()
    updates_str = get_alert_log_str(report_empty)
    print(updates_str)

    updates = get_alert_log()
    clear_alert_log()

    return updates


def watch_target(target_alias: str) -> list:
    _target = get_target_from_alias(target_alias)
    _target.watch()
    sort_alert_log()

    return get_alert_log()


def main():
    init()
    watch_targets(report_empty=True)


if __name__ == '__main__':
    main()
