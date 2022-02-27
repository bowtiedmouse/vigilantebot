from os.path import isfile
from typing import Union
import json
import logging

from vigilante.settings import TARGET_ACCOUNTS_FILE, VIGILANTE_LOG_FILE
from vigilante.holdings import holdings_file_exists, create_holdings_file
from vigilante.target import Target
from vigilante.alerts import get_alert_log, get_alert_log_str, clear_alert_log, sort_alert_log
from vigilante.fileutils import create_empty_json_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=VIGILANTE_LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(name)-10s: %(message)s'))
logger.addHandler(handler)
# logging.disable(logging.DEBUG)

# list of Targets to watch
_targets = []


def _get_target_accounts_data() -> dict:
    if not isfile(TARGET_ACCOUNTS_FILE):
        create_empty_json_file(TARGET_ACCOUNTS_FILE)
        logger.error(f"No target accounts found. Creating {TARGET_ACCOUNTS_FILE}")

    try:
        with open(TARGET_ACCOUNTS_FILE, "r") as f:
            target_accounts_data = json.load(f)
        return target_accounts_data

    except json.decoder.JSONDecodeError as e:
        logger.error(f"{TARGET_ACCOUNTS_FILE} file is malformed: {e}")


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


def get_targets_alias_list() -> list:
    return list(_get_target_accounts_data().keys())


def get_usd_balance_from_alias(alias: str) -> int:
    for _target in _targets:
        if _target.alias == alias:
            return _target.usd_balance
    return 0


def init() -> None:
    global _targets

    logger.info("Initializing targets...")

    if not holdings_file_exists():
        create_holdings_file()

    _targets = [
        Target(user["alias"], user["addresses"])
        for user in _get_target_accounts_data().values()
    ]

    logger.info("Targets ready.")


def watch_targets(print_results: bool = False) -> list:
    global _targets
    if not len(_targets):
        logger.warning('Targets are not initialized.')
        return ['no_targets']

    logger.info("Starting watch turn...")
    for _target in _targets:
        _target.watch()

    sort_alert_log()
    if print_results:
        updates_str = get_alert_log_str(print_results)
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
    watch_targets(print_results=True)


if __name__ == '__main__':
    main()
