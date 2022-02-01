#! /usr/bin/env python3
import json

from watcheduser import WatchedUser
from alerts import TokenAlertLog as Log
import alerts

# if watched_user had activity on etherscan:
#   for each account in watched_user:
#       by chain:
#       - symbol
#       - amount
#       - price
# compare with previous
# save

def main():
    with open("watched_accounts.json", "r") as watched_accounts_file:
        watched_accounts_data = json.load(watched_accounts_file)

    watched_accounts = [
        WatchedUser(user["alias"], user["address"])
        for user in watched_accounts_data
    ]

    for watched_user in watched_accounts:
        watched_user.watch()

    # TODO: alerts don't go here, just for testing
    Log.add(alerts.ChangedAlert(
        user_alias="Whale 1",
        chain_id="eth",
        symbol="ETH",
        amount_initial="1",
        amount_final="9")
    )
    Log.log()

    # for testing:
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
