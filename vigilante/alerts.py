from typing import Protocol
from dataclasses import dataclass, field
from pprint import pprint

# List to keep track of SortableAlert events
_log = []


class SortableAlert(Protocol):
    priority: int
    msg: str

    def log(self) -> None:
        pass

    def add(self, alert) -> None:
        pass


@dataclass(order=True)
class TokenBalanceAlert:
    """
    Represents an alert of activity in one token.

    Implements SortableAlert protocol.

    Is sortable. First by target_alias, then chain_id, then priority.
    """
    target_alias: str
    chain_id: str
    priority: int = field(init=False)
    msg: str = field(init=False, compare=False)

    @staticmethod
    def log():
        print(_log)

    @staticmethod
    def add(alert: str):
        _log.append(alert)


@dataclass
class RemovedAlert(TokenBalanceAlert):
    """
    Represents an alert for a token that has disappeared from a target's account.
    """
    symbol: str = field(repr=False)
    amount: str = field(repr=False)

    def __post_init__(self):
        self.priority = 1
        self.msg = (f"Token removed from account: {self.symbol}. "
                    f"Previous balance: {self.amount}")


@dataclass
class AddedAlert(TokenBalanceAlert):
    """
    Represents an alert for a new token that has been added to a target's account.
    """
    symbol: str = field(repr=False)
    amount: str = field(repr=False, compare=False)

    def __post_init__(self):
        self.priority = 2
        self.msg = f"New token on account: {self.symbol}. Balance: {self.amount}"


@dataclass
class ChangedAlert(TokenBalanceAlert):
    """
    Represents an alert for a token that has changed balance in a target's account.
    """
    symbol: str = field(repr=False)
    amount_initial: str = field(repr=False, compare=False)
    amount_final: str = field(repr=False, compare=False)

    def __post_init__(self):
        self.priority = 3
        self.msg = (f"Change in balance for token {self.symbol}: "
                    f"from {self.amount_initial} to {self.amount_final}")


class AlertLog:
    """
    Helps to interact with _log to update, sort or show it.
    """

    @staticmethod
    def add(alert: SortableAlert):
        _log.append(alert)

    @staticmethod
    def log():
        pprint(_log)

    @staticmethod
    def sort():
        global _log
        _log = sorted(_log,
                      key=lambda log_registry: (
                          log_registry.target_alias,
                          log_registry.chain_id,
                          log_registry.priority)
                      )


def log_target_holdings_changes(target_alias: str, diff: dict) -> None:
    """
    Public function to update the _log with new alerts from the DeepDiff data.

    :param target_alias: target alias
    :param diff: DeepDiff dictionary result
    :return: None
    """
    _log_diff_results(target_alias, diff['dictionary_item_removed'], action="removed")
    _log_diff_results(target_alias, diff['dictionary_item_added'], action="added")
    _log_diff_results(target_alias, diff['values_changed'], action="changed")


def _log_diff_results(target_alias: str, diff_results: dict, action: str):
    """
    Logs DeepDiff data to the alert system.

    DeepDiff model:
    {
        'dictionary_item_added':    {"root['arb']['WETH']": '0.661955993077381'},
        'dictionary_item_removed':  {"root['eth']['PDT']": '475.63850932673466'},
        'values_changed':           {"root['arb']['DPX']":{
                                        'new_value': '10.23860662271384542',
                                        'old_value': '0.23860662271384542'},
                                    "root['eth']['FTM']": {
                                        'new_value': '68.84653761752556',
                                        'old_value': '69.84653761752556'}
                                    }
    }
    """
    for chain_token, balance in diff_results.items():
        try:
            # DeepDiff has a extract() function, but it only returns value,
            # and we also need key
            chain_id, symbol = chain_token.replace(
                "root['", "").replace("']", "").split("['")
            _add_alert(action, target_alias, chain_id, symbol, balance)

        except ValueError:
            # If a target adds tokens to a new chain the format returned from DeepDiff
            # will be different
            chain_id = chain_token.replace("root['", "").replace("']", "")
            for symbol, amount in balance.items():
                _add_alert(action, target_alias, chain_id, symbol, amount)


def _add_alert(action: str, target_alias: str, chain_id: str, symbol: str, amount):
    if action == "removed":
        AlertLog.add(RemovedAlert(target_alias, chain_id, symbol, amount))

    elif action == "added":
        AlertLog.add(AddedAlert(target_alias, chain_id, symbol, amount))

    elif action == "changed":
        AlertLog.add(ChangedAlert(target_alias, chain_id, symbol,
                                  amount_initial=amount['old_value'],
                                  amount_final=amount['new_value']
                                  ))
