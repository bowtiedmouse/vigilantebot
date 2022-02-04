import re
from typing import Protocol
from dataclasses import dataclass, field

# List to keep track of SortableAlert events
_log = []


class SortableAlert(Protocol):
    priority: int
    msg: str

    def log(self) -> None:
        pass


@dataclass(order=True)
class TokenAlert:
    """
    Represents an alert of activity in one token.

    Implements SortableAlert protocol.

    Is sortable. First by target_alias, then chain_id, then priority.
    """
    target_alias: str
    chain_id: str
    priority: int = field(init=False, repr=False)
    msg: str = field(init=False, compare=False, repr=False)

    def log(self) -> None:
        print(self.msg)


@dataclass
class NewTargetAlert(TokenAlert):
    """
    Represents an alert for a new target added to the watch.
    """
    usd_balance: int = field(compare=False)
    token_list: list = field(compare=False)
    # needed for sorting:
    chain_id: str = field(init=False, repr=False, default="")

    def __post_init__(self):
        self.priority = 90
        self.msg = (f"Added to file. "
                    f"Current USD balance: ${'{:,}'.format(self.usd_balance)}. "
                    f"Token holdings: {', '.join(self.token_list)}")


@dataclass
class USDBalanceAlert(TokenAlert):
    """
    Not really an alert, but helps with logging a target's USD balance.
    """
    balance: int = field(compare=False)
    # needed for sorting:
    chain_id: str = field(init=False, repr=False, default="")

    def __post_init__(self):
        self.priority = 5
        self.msg = (f"Total USD balance: "
                    f"${'{:,}'.format(self.balance)}")


@dataclass
class RemovedAlert(TokenAlert):
    """
    Represents an alert for a token that has disappeared from a target's account.
    """
    symbol: str
    amount: str = field(repr=False)

    def __post_init__(self):
        self.priority = 10
        self.msg = (f"Token removed: {self.chain_id}.{self.symbol}. "
                    f"Previous balance: {self.amount}")


@dataclass
class AddedAlert(TokenAlert):
    """
    Represents an alert for a new token that has been added to a target's account.
    """
    symbol: str
    amount: str = field(repr=False, compare=False)

    def __post_init__(self):
        self.priority = 20
        self.msg = f"New token: {self.chain_id}.{self.symbol}. Balance: {self.amount}"


@dataclass
class ChangedAlert(TokenAlert):
    """
    Represents an alert for a token that has changed balance in a target's account.
    """
    symbol: str
    amount_previous: str = field(compare=False)
    amount_new: str = field(compare=False)

    def __post_init__(self):
        self.priority = 30
        self.msg = (f"Balance changed for {self.chain_id}.{self.symbol}: "
                    f"from {self.amount_previous} to {self.amount_new}")


class AlertLog:
    """
    Helps to interact with _log to update, sort or show it.
    """

    @staticmethod
    def add(alert: SortableAlert):
        _log.append(alert)

    @staticmethod
    def log():
        if len(_log) == 0:
            print("No updates to report on watched targets yet.")
            return False

        last_alias = ""
        for alert in _log:
            if last_alias != alert.target_alias:
                print(f"\nUpdates for **{alert.target_alias}**:")
                last_alias = alert.target_alias

            print("·", end=" ")
            alert.log()

    @staticmethod
    def sort():
        global _log
        _log = sorted(_log,
                      key=lambda log_registry: (
                          log_registry.target_alias,
                          log_registry.chain_id,
                          log_registry.priority)
                      )


def log_new_target(target_alias: str, balance: float, target_holdings: dict):
    token_list = [token for chain in target_holdings.values() for token in chain]
    AlertLog.add(NewTargetAlert(target_alias, int(balance), token_list))
    # return token_list  # for testing


def log_target_holdings_diff(target_alias: str, diff: dict) -> None:
    """
    Public function to update the _log with new alerts from the DeepDiff data.

    :param target_alias: target alias
    :param diff: DeepDiff dictionary result
    :return: None
    """
    if 'dictionary_item_removed' in diff:
        _log_diff_results(target_alias, diff['dictionary_item_removed'],
                          action="removed")
    if 'dictionary_item_added' in diff:
        _log_diff_results(target_alias, diff['dictionary_item_added'], action="added")
    if 'values_changed' in diff:
        _log_diff_results(target_alias, diff['values_changed'], action="changed")


def log_target_usd_balance(target_alias: str, balance: int) -> None:
    """
    Adds the current USD balance of a target account to the logs.

    :param target_alias: target alias
    :param balance: USD balance
    :return: None
    """
    AlertLog.add(USDBalanceAlert(target_alias, balance))


def _log_diff_results(target_alias: str, diff_results: dict, action: str):
    """
    Logs DeepDiff data to the alert system.

    DeepDiff model (assuming comparing inside target's holdings key):
    {
        'dictionary_item_added': {
            "root['arb']['DPX']": {
                    'amount': '51.344',
                    'contract_address': '0x1aa61c196e76805fcbe394ea00e4ffced24fc420',
                    'symbol': 'DPX',
                    'usd_price': '1668.29'}},
        'dictionary_item_removed': {
            "root['arb']['MAGIC']": {
                    'amount': 1551.344,
                    'contract_address': '0x1aa61c196e76805fcbe394ea00e4ffced24fc469',
                    'symbol': 'MAGIC',
                    'usd_price': 8.29}},
        'values_changed': {
            "root['eth']['ETH']['amount']": {
                    'new_value': 3.3440000000000003,
                    'old_value': 1.344}}
    }
    """
    for path, token_data in diff_results.items():
        # try:
        path_keys = re.compile(r'[a-zA-Z]+').findall(path)
        chain_id = path_keys[1]
        symbol = path_keys[2]
        _add_alert(action, target_alias, chain_id, symbol, token_data)

        # except ValueError:
        #     # If a target adds tokens to a chain that didn't exist before, the format
        #     # returned from DeepDiff will be different
        #     chain_id = chain_token.replace("root['", "").replace("']", "")
        #     for symbol, amount in balance.items():
        #         _add_alert(action, target_alias, chain_id, symbol, amount)


def _add_alert(action: str, target_alias: str, chain_id: str, symbol: str, token_data: dict) -> None:
    assert action in {'removed', 'added', 'changed'}, "Wrong action supplied."

    if action == "removed":
        AlertLog.add(RemovedAlert(target_alias, chain_id,
                                  symbol, token_data['amount']))

    elif action == "added":
        AlertLog.add(AddedAlert(target_alias, chain_id,
                                symbol, token_data['amount']))

    elif action == "changed":
        AlertLog.add(ChangedAlert(target_alias, chain_id, symbol,
                                  amount_previous=token_data['old_value'],
                                  amount_new=token_data['new_value']
                                  ))
