from collections import defaultdict, deque
from functools import partial

import augustus as ag
from augustus.system.base_cleaner import CleanerBase


class SMA(CleanerBase):
    def calculate(self, ticker):
        key = f'{ticker}_{self.frequency}'
        close = self.data[key]['close']

        return sum(close)/len(close)  
