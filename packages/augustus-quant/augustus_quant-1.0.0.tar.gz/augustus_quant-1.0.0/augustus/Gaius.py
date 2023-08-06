import logging
import sys

import arrow

from augustus.builtin.optimizer import Optimizer
from augustus.config import EVENT_LOOP
from augustus.constants import EVENT
from augustus.custom.forward_analysis import ForwardAnalysis
from augustus.system.components.exceptions import BacktestFinished
from augustus.system.components.logger import LoggerFactory
from augustus.system.components.market_maker import MarketMaker
from augustus.system.components.order_checker import PendingOrderChecker
from augustus.system.components.output import OutPut
from augustus.system.metabase_env import augustusEnvBase
from augustus.utils.awesome_func import show_process


class Gaius(augustusEnvBase):
    def __init__(self):
        self.market_maker: MarketMaker = None
        self.pending_order_checker: PendingOrderChecker = None
        self.event_loop: list = None

        self.optimizer = Optimizer()
        self.forward_analysis = ForwardAnalysis()

    def _pre_initialize_trading_system(self):
        self.event_loop = EVENT_LOOP
        self.market_maker = MarketMaker()
        self.pending_order_checker = PendingOrderChecker()

    def initialize_trading_system(self):  
        self._pre_initialize_trading_system()
        self.env.initialize_env()
        self.market_maker.initialize()
        self.env.recorder.initialize()

    def sunny(self, summary: bool = True, show_process: bool = False):
        self.initialize_trading_system()

        while True:
            try:
                if self.env.event_engine.is_empty():
                    self.market_maker.update_market()
                    self.pending_order_checker.run()

                    if show_process:
                        self._show_process()
                else:
                    cur_event = self.env.event_engine.get()
                    self._run_event_loop(cur_event)

            except BacktestFinished:
                if summary:
                    print("\n")
                    self.output.summary()

                break

    def _run_event_loop(self, cur_event):
        for element in self.event_loop:
            if self._event_is_executed(cur_event, **element):
                break

    def _event_is_executed(
        self, cur_event, if_event: EVENT, then_event: EVENT, module_dict: dict
    ) -> bool:

        if cur_event is None:
            return True

        elif cur_event == if_event:
            [value.run() for value in module_dict.values()]
            self.env.event_engine.put(then_event)

            return True
        else:
            return False

    def _show_process(self):
        fromdate = arrow.get(self.env.fromdate)
        todate = arrow.get(self.env.todate)
        curdate = arrow.get(self.env.sys_date)
        total_days = (todate - fromdate).days
        finished_days = (curdate - fromdate).days
        show_process(finished_days, total_days)

    def set_date(self, fromdate: str, todate: str, frequency: str, instrument: str):
        """
        Instrument: A_shares, Forex
        Frequency:
                (S5, S10, S30, M1, M2, M4, M5) <- BAD Interval
                M10, M15, M30, H1, H2, H3, H4, H6, H8, H12
        """
        self.env.instrument = instrument
        self.env.fromdate = fromdate
        self.env.todate = todate
        self.env.sys_frequency = frequency

    def set_forex_live_trading(self, frequency: str):
        """
        Frequency:
                (S5, S10, S30, M1, M2, M4, M5) <- BAD Interval
                M10, M15, M30, H1, H2, H3, H4, H6, H8, H12
        """
        fromdate = arrow.utcnow().format("YYYY-MM-DD HH:mm:ss")
        self.set_date(fromdate, None, frequency, "Forex")
        self.env.sys_date = fromdate
        self.env.is_live_trading = True

    def show_today_signals(self):
        
        self.env.is_show_today_signals = True

    @classmethod
    def show_log(cls, file=False, no_console=False):
        if file:
            LoggerFactory("augustus")

        if no_console:
            logging.getLogger("augustus").propagate = False
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def set_recursion_limit(cls, limit: int = 2000):
        
        sys.setrecursionlimit(limit)

    def save_original_signal(self):
        self.env.is_save_original = True

    @property
    def output(self) -> OutPut:
        return OutPut()
