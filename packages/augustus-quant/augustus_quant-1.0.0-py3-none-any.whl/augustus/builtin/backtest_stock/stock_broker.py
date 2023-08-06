from augustus.builtin.backtest_stock.stock_limit_filter_risk_manager import \
    StockLimitFilterRiskManager
from augustus.system.base_broker import BrokerBase
from augustus.system.models.orders.general_order import MarketOrder


class StockBroker(BrokerBase):

    def __init__(self):
        super().__init__()
        StockLimitFilterRiskManager()

    @classmethod
    def _required_cash_func(cls, order: MarketOrder) -> float:
        # TODO：还要加上手续费,和保证金

        return order.size * order.execute_price
