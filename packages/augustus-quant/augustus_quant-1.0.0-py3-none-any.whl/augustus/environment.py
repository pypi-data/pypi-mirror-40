import logging
from collections import defaultdict

import arrow

import augustus as ag
from augustus.event_engine import EventEngine
from augustus.utils.easy_func import get_day_ratio


class Environment(object):

    # general context
    sys_date: str = None
    sys_frequency: str = None
    instrument: str = None
    fromdate: str = None
    todate: str = None
    tickers: list = []

    # general setting
    execute_on_close_or_next_open: str = 'open'
    is_save_original: bool = False      
    is_live_trading: bool = False
    is_show_today_signals: bool = False  

    # backtest modules dict
    readers: dict = {}
    feeds: dict = {}
    cleaners: dict = {}
    cleaners_feeds: dict = {}
    strategies: dict = {}
    brokers: dict = {}
    risk_managers: dict = {}
    recorders: dict = {}
    recorder = None  # type: op.RecorderBase

    # system memory
    signals_normal: list = []  
    signals_pending: list = []  
    signals_trigger: list = []  
    signals_cancel: list = []  

    signals_normal_cur: list = []
    signals_pending_cur: list = []
    signals_trigger_cur: list = []
    signals_cancel_cur: list = []

    orders_mkt_normal_cur: list = []  
    orders_child_of_mkt_dict: dict = {}  
    orders_mkt_absolute_cur: list = []  
    orders_mkt_submitted_cur: list = []  

    orders_pending: list = []   

    orders_cancel_cur: list = []  
    orders_cancel_submitted_cur: list = []  

    cur_suspended_tickers: list = []  
    suspended_tickers_record: defaultdict = defaultdict(list)  

    # system modules
    logger = logging.getLogger("augustus")
    event_engine = EventEngine()
    cache: dict = {}

    @classmethod
    def initialize_env(cls):
        cls.signals_normal.clear()
        cls.signals_pending.clear()
        cls.signals_trigger.clear()
        cls.signals_cancel.clear()
        cls.signals_normal_cur.clear()
        cls.signals_pending_cur.clear()
        cls.signals_trigger_cur.clear()
        cls.signals_cancel_cur.clear()
        cls.orders_mkt_normal_cur.clear()
        cls.orders_mkt_absolute_cur.clear()
        cls.orders_mkt_submitted_cur.clear()
        cls.orders_pending.clear()
        cls.orders_child_of_mkt_dict.clear()
        cls.orders_cancel_cur.clear()
        cls.orders_cancel_submitted_cur.clear()
        cls.tickers.clear()
        cls.cur_suspended_tickers.clear()
        cls.suspended_tickers_record.clear()
        cls.cache.clear()

        if not cls.is_live_trading:
            ratio = get_day_ratio(cls.sys_frequency)
            cls.sys_date = arrow.get(cls.fromdate).shift(
                days=-ratio).format('YYYY-MM-DD HH:mm:ss')
        cls.reset_all_counters()

    @classmethod
    def clear_modules(cls):
        cls.sys_date: str = None
        cls.sys_frequency: str = None

        cls.instrument: str = None
        cls.fromdate: str = None
        cls.todate: str = None
        cls.tickers: list = []
        cls.cur_suspended_tickers: list = []
        cls.suspended_tickers_record: defaultdict = defaultdict(list)

        cls.market_maker = None
        cls.readers: dict = {}
        cls.feeds: dict = {}
        cls.cleaners: dict = {}
        cls.cleaners_feeds: dict = {}
        cls.strategies: dict = {}
        cls.brokers: dict = {}
        cls.risk_managers: dict = {}
        cls.recorders: dict = {}
        cls.recorder = None  # type: op.RecorderBase

        cls.event_loop = None  # type:  List[Dict]
        cls.cache = {}

        cls.execute_on_close_or_next_open: str = 'open'
        cls.is_save_original: bool = False
        cls.is_live_trading: bool = False
        cls.is_show_today_signals: bool = False

    @classmethod
    def reset_all_counters(cls):
        from itertools import count
        from augustus.system.models import signals
        from augustus.system.base_cleaner import CleanerBase
        from augustus.system.models.orders.base_order import OrderBase
        from augustus.system.components.order_generator import OrderGenerator
        CleanerBase.counter = count(1)
        signals.Signal.counter = count(1)
        signals.SignalByTrigger.counter = count(1)
        signals.SignalForPending.counter = count(1)
        signals.SignalCancelTST.counter = count(1)
        signals.SignalCancelPending.counter = count(1)
        OrderBase.counter = count(1)
        OrderGenerator.counter = count(1)