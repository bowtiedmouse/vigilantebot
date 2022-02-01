from typing import Protocol
from dataclasses import dataclass, field

_log = []


# Use:
# VigilanteLog.add(ChangedAlert("Whale 1", "ETH", "1", "2"))
# VigilanteLog.add(AddedAlert("Whale 2", "ETH", "10"))
# VigilanteLog.add(RemovedAlert("Whale 1", "MAGIC", "1"))
# VigilanteLog.sort()
# VigilanteLog.log()


class SortableAlert(Protocol):
    priority: int
    msg: str

    def log(self) -> None:
        pass

    def add(self, alert) -> None:
        pass


@dataclass(order=True)
class TokenBalanceAlert:
    """Represents an alert of activity in one token.

    Implements SortableAlert protocol.

    Is sortable. First by user_alias, then chain_id, then priority."""
    user_alias: str
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
    symbol: str = field(repr=False)
    amount: str = field(repr=False)

    def __post_init__(self):
        self.priority = 1
        self.msg = f"Token removed from account: {self.symbol}. Balance: {self.amount}"


@dataclass
class AddedAlert(TokenBalanceAlert):
    symbol: str = field(repr=False)
    amount: str = field(repr=False, compare=False)

    def __post_init__(self):
        self.priority = 2
        self.msg = f"New token on account: {self.symbol}. Balance: {self.amount}"


@dataclass
class ChangedAlert(TokenBalanceAlert):
    symbol: str = field(repr=False)
    amount_initial: str = field(repr=False, compare=False)
    amount_final: str = field(repr=False, compare=False)

    def __post_init__(self):
        self.priority = 3
        self.msg = f"Change in balance for token {self.symbol}: from {self.amount_initial} to {self.amount_final}"


class TokenAlertLog:
    @staticmethod
    def add(alert: SortableAlert):
        _log.append(alert)

    @staticmethod
    def log():
        print(_log)

    @staticmethod
    def sort():
        global _log
        _log = sorted(_log,
                      key=lambda log_registry: (
                          log_registry.user_alias,
                          log_registry.chain_id,
                          log_registry.priority)
                      )
