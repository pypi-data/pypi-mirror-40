from augustus.builtin.backtest_forex.forex_bar import BarForex
from augustus.builtin.backtest_stock.stock_bar import BarAshares
from augustus.constants import EVENT
from augustus.system.metabase_env import augustusEnvBase

EVENT_LOOP = [dict(if_event=EVENT.Market_updated,
                   then_event=EVENT.Data_cleaned,
                   module_dict=augustusEnvBase.env.cleaners),

              dict(if_event=EVENT.Data_cleaned,
                   then_event=EVENT.Signal_generated,
                   module_dict=augustusEnvBase.env.strategies),

              dict(if_event=EVENT.Signal_generated,
                   then_event=EVENT.Submit_order,
                   module_dict=augustusEnvBase.env.risk_managers),

              dict(if_event=EVENT.Submit_order,
                   then_event=EVENT.Record_result,
                   module_dict=augustusEnvBase.env.brokers),

              dict(if_event=EVENT.Record_result,
                   then_event=None,
                   module_dict=augustusEnvBase.env.recorders)]