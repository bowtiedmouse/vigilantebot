#! /usr/bin/env python3
import json

import settings
from target import Target
from alerts import AlertLog as Log


# if watched_user had activity on etherscan:
#   for each account in watched_user:
#       by chain:
#       - symbol
#       - amount
#       - price
# compare with previous
# save

def main():
    with open(settings.TARGET_ACCOUNTS_FILE, "r") as f:
        target_accounts_data = json.load(f)

    targets = [
        Target(user["alias"], user["addresses"])
        for user in target_accounts_data
    ]

    for target in targets:
        target.watch()

    Log.log()


if __name__ == '__main__':
    main()
