import json
import requests
from dataclasses import dataclass, field
import settings
import time
import utils
import alerts
from alerts import TokenAlertLog as Log


# On object init: check if exists on file?
# 0- check timestamp of last tx and compare with user last_active in file
# 1- process tokens to merge all accounts from one user DONE
# 2- compare with user saved in file
# 3- log differences
# 4- update file

#   Note: a different in a token balance could mean he's staking/unstaking it or claiming
#   No need for updating the file: just load it in memory, compare with response, and dump the new data

@dataclass
class WatchedUser:
    # todo: reconsider properties and methods to avoid overload
    alias: str
    address: list
    holdings: dict = field(init=False, default_factory=dict)
    usd_balance: int = field(init=False, default=0)
    last_active: int = field(init=False, default=0)
    token_updates: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.holdings = {
            "alias": self.alias,
            "usd_balance": self.usd_balance,
            "last_active": self.last_active,
            "tokens_by_chain": {}
        }

    def watch(self):
        # todo: should be async
        # while True:
        if self.has_updates():
            self.update()
            # compare()
            # TODO: alerts don't go here, just for testing
            Log.add(alerts.ChangedAlert(
                user_alias="Whale 1",
                chain_id="eth",
                symbol="ETH",
                amount_initial="1",
                amount_final="9")
            )
            utils.update_balances_file(self.alias, self.holdings)
            # time.sleep(10 * 60)

    def update(self):
        # print(f"\nBalances for {self.alias}:")
        # print("===========================")
        for account in self.address:
            tokens = utils.request_token_list(account)
            self.process_token_list(tokens.json())
            self.usd_balance += utils._get_account_usd_balance(account)

    def process_token_list(self, tokens):
        """Simplifies request's returned object by getting only needed data and
        merging tokens balances from different user's accounts.
        """
        # print("Processing data...")
        tokens_by_chain = self.holdings["tokens_by_chain"]

        for token in tokens:
            if not utils._has_min_token_balance(token):
                continue

            chain_id = token["chain"].lower()
            symbol = token["symbol"].upper()
            amount = token["amount"]

            if chain_id not in tokens_by_chain:
                tokens_by_chain[chain_id] = {}

            if symbol in tokens_by_chain[chain_id]:
                # print(f"Merging {symbol} from {tokens_by_chain[chain_id][symbol]} with {amount}")
                amount += float(tokens_by_chain[chain_id][symbol])
            tokens_by_chain[chain_id][symbol] = str(amount)

        self.holdings["tokens_by_chain"] = tokens_by_chain

    # deprecated?
    def print_tokens(self, account_tokens):
        tokens = account_tokens.json()
        last_chain = tokens[0]["chain"]
        print(f"Tokens on {last_chain.title()}:")

        self.holdings["alias"] = self.alias
        # self.token_list["usd_balance"] = self._get_account_balance(tokens)
        for token in tokens:
            if not utils._has_min_token_balance(token):
                continue

            if token["chain"] != last_chain:
                last_chain = token["chain"]
                print(f"Tokens on {last_chain.title()}:")
            print(f"· {token['amount']} of {token['symbol']}")
        #       by chain:
        #       - symbol
        #       - amount
        #       - price

    def get_last_active(self):
        """Check for watching file, get user's last_active timestamp"""

    def has_updates(self):
        """Compares last_active from get_last_active with etherscan/ftmscan/arbiscan/avax last tx"""
        return True

