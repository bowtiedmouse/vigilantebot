import time
from dataclasses import dataclass

import settings
import holdings
import alerts


@dataclass
class Target:
    """
    Represents a user that is being watched.
    """
    alias: str
    addresses: list

    def watch(self) -> None:
        print(f"Watching {self.alias}...")
        new_target = not holdings.is_target_in_file(self.alias)

        # todo: only for testing
        test = True
        # todo: should be async
        while test:
            updated_holdings = self.get_updated_holdings()
            usd_balance = self.get_usd_balance()

            if new_target:
                self._save_new_target(usd_balance, updated_holdings)
                new_target = False

                continue

            holdings_diff = holdings.get_target_holdings_diff(
                self.alias, updated_holdings)

            if holdings_diff:
                alerts.log_target_holdings_diff(self.alias, holdings_diff)
                alerts.log_target_usd_balance(self.alias, usd_balance)
                self._update_file(updated_holdings, usd_balance)

            # time.sleep(settings.WATCH_FREQUENCY)
            test = False

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

    def _update_file(self, updated_holdings: dict, usd_balance: int) -> None:
        holdings.update_holdings_file(self.alias, updated_holdings, usd_balance)

    def _save_new_target(self, usd_balance: int, updated_holdings: dict):
        alerts.log_new_target(self.alias, usd_balance, updated_holdings)
        print(f"{self.alias} holdings will be added to {settings.TARGETS_HOLDINGS_FILE}")
        self._update_file(updated_holdings, usd_balance)