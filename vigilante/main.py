#! /usr/bin/env python3
import os
import json

import settings
from target import Target
from alerts import AlertLog as Log


#   for each account in watched_user:
#       by chain:
#       - symbol
#       - amount
#       - price
# compare with previous
# save

def _get_target_accounts_data() -> dict:
    assert os.path.isfile(settings.TARGET_ACCOUNTS_FILE), "Need some accounts to watch!"

    try:
        with open(settings.TARGET_ACCOUNTS_FILE, "r") as f:
            target_accounts_data = json.load(f)
        return target_accounts_data

    except json.decoder.JSONDecodeError as e:
        print(f"{settings.TARGET_ACCOUNTS_FILE} file is malformed: {e}")


def main():
    targets = [
        Target(user["alias"], user["addresses"])
        for user in _get_target_accounts_data()
    ]

    for target in targets:
        target.watch()

    Log.sort()
    Log.log()


if __name__ == '__main__':
    main()
