#! /usr/bin/env python3
import json
import requests
from dataclasses import dataclass, field
import settings
import time

import alerts
from watcheduser import WatchedUser
from alerts import TokenAlertLog as Log


# if watched_user had activity on etherscan:
#   for each account in watched_user:
#       by chain:
#       - symbol
#       - amount
#       - price
# compare with previous
# save

# def update_file():
#     with open('my_file.json', 'r') as f:
#         json_data = json.load(f)
#         json_data['b'] = "9"
#
#     with open('my_file.json', 'w') as f:
#         f.write(json.dumps(json_data))


def _has_min_token_balance(token: json):
    return token['amount'] * token['price'] >= settings.MIN_TOKEN_BALANCE


def _get_account_usd_balance(account):
    balance = requests.get(settings.DEBANK_ACCOUNT_BALANCE_URL.format(address=account)).json()["total_usd_value"]
    return int(balance)


def request_token_list(account):
    # print("Requesting data from Debank...")
    return requests.get(settings.DEBANK_TOKEN_LIST_URL.format(address=account))


def update_balances_file(user_alias: str, user_holdings: dict):
    with open(settings.WALLETS_BALANCE_FILE, "w") as f:
        print("Updating file...")
        json.dump(user_holdings, f)


def get_balances_from_file(user_alias: str) -> dict:
    with open(settings.WALLETS_BALANCE_FILE, "r") as f:
        return json.load(f)


def compare_last_balances_with_prev(user_alias, current_holdings):
    prev = get_balances_from_file(user_alias)


def main():
    with open("watched_accounts.json", "r") as watched_accounts_file:
        watched_accounts_data = json.load(watched_accounts_file)

    watched_accounts = [
        WatchedUser(user["alias"], user["address"])
        for user in watched_accounts_data
    ]

    for watched_user in watched_accounts:
        watched_user.watch()

    Log.log()

    # tokens = {
    #     "tokens_by_chain": {
    #         "eth": {
    #             "ETH": "1.223",
    #             "WILD": "232"
    #         },
    #         "arb": {
    #             "ETH": "1.223",
    #             "MAGIC": "1232"
    #         }
    #     }
    # }
    #
    # for i in range(5):
    #     tokens["tokens_by_chain"]["eth"]["MAGIC_" + str(i)] = i
    # tokens["tokens_by_chain"]["eth"]["dpx"] = 508
    # print(tokens)
    # for symbol, amount in tokens["tokens_by_chain"]["eth"].items():
    #     print(f"{amount} {symbol}")


if __name__ == '__main__':
    main()
