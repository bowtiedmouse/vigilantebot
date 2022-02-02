import time
from dataclasses import dataclass

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

    def watch(self) -> None:
        # todo: should be async
        # while True:
        # 1. Get updated balances data
        holdings_by_chain = self.get_updated_holdings()
        # 2. Compare with previously saved data
        changes = compare.get_target_holdings_changes(self.alias, holdings_by_chain)
        usd_balance = self.get_usd_balance()
        # 4. Add differences to the log
        alerts.log_target_holdings_changes(self.alias, changes)
        alerts.log_target_usd_balance(self.alias, usd_balance)
        # 3. Update saved data
        holdings.update_holdings_file(self.alias, holdings_by_chain, usd_balance)
        # time.sleep(settings.WATCH_FREQUENCY)

    def get_updated_holdings(self) -> dict:
        """
        Gets last updated aggregated holdings for all the accounts of a target.

        :return: dict
        """
        holdings_by_chain = {}
        for account in self.addresses:
            holdings_by_chain = holdings.get_token_holdings(account, holdings_by_chain)
        return holdings_by_chain

    def get_usd_balance(self) -> int:
        """
        Gets the total USD balance of all the accounts of a target.

        :return: int
        """
        return sum(
            holdings.get_account_usd_balance(account) for account in self.addresses
        )