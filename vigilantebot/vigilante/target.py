from dataclasses import dataclass, field
import logging

from vigilante import settings
from vigilante import holdings
from vigilante import alerts

logger = logging.getLogger(__name__)


@dataclass
class Target:
    """
    Represents a user that is being watched.
    """
    alias: str
    addresses: list
    usd_balance: int = field(init=False)
    holdings: dict = field(init=False)

    def watch(self) -> None:
        logger.debug(f'Getting updates for {self.alias}...')
        self._update()
        # logger.debug('Ended request updates with result %s', self.holdings)

        if not holdings.is_target_in_file(self.alias):
            self._save_new_target()
            return

        holdings_diff = holdings.get_target_holdings_diff(self.alias, self.holdings)
        if holdings_diff:
            self._log_diff(holdings_diff)
            self._update_file()
            # logger.debug('Holdings diff for %s: %s', self.alias, holdings_diff)

    def _update(self):
        self.holdings = self._get_updated_holdings()
        self.usd_balance = self._get_usd_balance()

    def _get_updated_holdings(self) -> dict:
        """
        Gets last updated aggregated holdings for all the accounts of a target.

        :return: dict
        """
        holdings_by_chain = {}
        for account in self.addresses:
            holdings_by_chain = holdings.get_token_holdings(account, holdings_by_chain)
        return holdings_by_chain

    def _get_usd_balance(self) -> int:
        return holdings.get_target_usd_balance(self)

    def _log_diff(self, holdings_diff) -> None:
        alerts.log_target_holdings_diff(self, holdings_diff)
        alerts.log_target_usd_balance(self.alias, self.usd_balance)

    def _update_file(self) -> None:
        holdings.update_holdings_file(self.alias, self.holdings, self.usd_balance)

    def _save_new_target(self) -> None:
        alerts.log_new_target(self.alias, self.usd_balance, self.holdings)
        logger.info(f"{self.alias} holdings will be added to {settings.TARGETS_HOLDINGS_FILE}")
        self._update_file()
