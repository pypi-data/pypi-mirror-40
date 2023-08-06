import abc

from dataclasses import dataclass, field

from augustus.constants import ActionType
from augustus.system.metabase_env import augustusEnvBase
from augustus.system.models.signals import SignalByTrigger


@dataclass
class TradeLogBase(augustusEnvBase, abc.ABC):

    buy: float = None
    sell: float = None
    size: float = None

    entry_date: str = field(init=False)
    exit_date: str = field(init=False)

    entry_price: float = field(init=False)
    exit_price: float = field(init=False)

    entry_type: str = field(init=False)
    exit_type: str = field(init=False)

    pl_points: float = field(init=False)
    re_pnl: float = field(init=False)

    commission: float = field(init=False)

    @abc.abstractmethod
    def generate(self):
        raise NotImplementedError

    def _earn_short(self):
        return -1 if self.buy.action_type == ActionType.Short else 1

    @staticmethod
    def _get_order_type(order):
        if isinstance(order.signal, SignalByTrigger):
            return order.signal.order_type.value
        else:
            return order.order_type.value

    @abc.abstractmethod
    def settle_left_trade(self):
        raise NotImplementedError

    @property
    def ticker(self):
        return self.buy.ticker
