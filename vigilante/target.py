import time
from dataclasses import dataclass, field

import holdings
import compare
import alerts


# On object init: check if exists on file?
# 0- check timestamp of last tx and compare with user last_active in file
# 1- process tokens to merge all accounts from one user DONE
# 2- compare with user saved in file
# 3- log differences
# 4- update file

# Note: a different in a token balance could mean he's staking/unstaking it or claiming
# No need for updating the file: just load it in memory, compare with response, and dump
#   the new data


@dataclass
class Target:
    """
    Represents a user that is being watched.
    """
    alias: str
    addresses: list
    holdings: dict = field(init=False, default_factory=dict)
    # usd_balance: int = field(init=False, default=0)
    # last_active: int = field(init=False, default=0)

    def __post_init__(self):
        self.holdings = {
            "alias": self.alias,
            # "usd_balance": self.usd_balance,
            # "last_active": self.last_active,
            "tokens_by_chain": {}
        }

    def watch(self):
        # todo: should be async
        # while True:
        # if self.has_updates():
        # 1. Get updated balances data
        self.update_holdings()
        # 2. Compare with previously saved data
        changes = compare.get_target_holdings_changes(self.alias, self.holdings)
        # 4. Add differences to the log
        alerts.log_target_holdings_changes(self.alias, changes)
        # 3. Update saved data
        # holdings.update_holdings_file(self.alias, self.holdings)
        # time.sleep(settings.WATCH_FREQUENCY)

    def update_holdings(self):
        for account in self.addresses:
            self.holdings['tokens_by_chain'] = holdings.get_token_holdings(account)
            # todo: usd_balance probably not needed here
            # self.usd_balance += holdings.get_account_usd_balance(account)

    # todo: if don't use has_updates, this will be gone
    def get_last_active(self):
        """
        Check for watching file, get user's last_active timestamp.
        """

    # todo: probably not needed: would be easier to just request holdings every time
    def has_updates(self):
        """
        Compares last_active from get_last_active with etherscan/ftmscan/arbiscan/avax last tx.
        """
        return True
