#! /usr/bin/env python3
import os
import json

import settings
from holdings import holdings_file_exists, create_holdings_file
from target import Target
from alerts import AlertLog as Log

# list of Targets to watch
_targets = []


def _get_target_accounts_data() -> dict:
    assert os.path.isfile(settings.TARGET_ACCOUNTS_FILE), "Need some accounts to watch!"

    try:
        with open(settings.TARGET_ACCOUNTS_FILE, "r") as f:
            target_accounts_data = json.load(f)
        return target_accounts_data

    except json.decoder.JSONDecodeError as e:
        print(f"{settings.TARGET_ACCOUNTS_FILE} file is malformed: {e}")


def init():
    global _targets

    print("Initializing targets...")

    if not holdings_file_exists():
        create_holdings_file()

    _targets = [
        Target(user["alias"], user["addresses"])
        for user in _get_target_accounts_data()
    ]


def watch_targets():
    global _targets
    if not len(_targets):
        init()

    print("Starting watch turn...")
    for target in _targets:
        target.watch()

    Log.sort()
    Log.log()


def main():
    init()
    watch_targets()


if __name__ == '__main__':
    main()