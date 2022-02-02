#! /usr/bin/env python3
import json

import settings
from target import Target
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
    with open(settings.TARGET_ACCOUNTS_FILE, "r") as f:
        target_accounts_data = json.load(f)

    targets = [
        Target(user["alias"], user["address"])
        for user in target_accounts_data
    ]

    for target in targets:
        target.watch()

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
