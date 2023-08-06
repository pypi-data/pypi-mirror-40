from augustus.constants import ActionType
from augustus.system.models.base_series import (CommissionSeriesBase,
                                                 HoldingPnlSeriesBase,
                                                 MarginSeriesBase,
                                                 MarketValueSeriesBase,
                                                 RealizedPnlSeriesBase)


class RealizedPnlSeries(RealizedPnlSeriesBase):
    name = 'realized_pnl'
    def update_order(self, ticker, size, execute_price, action_type,
                     last_avg_price,  long_or_short='long'):
        new_value = None

        if action_type == ActionType.Sell:
            new_value = (self.latest(ticker, long_or_short) +
                         (execute_price - last_avg_price) * size)
        elif action_type == ActionType.Cover:
            new_value = (self.latest(ticker, long_or_short) -
                         (execute_price - last_avg_price) * size)

        if new_value:
            self._append_value(ticker, new_value, long_or_short)


class CommissionSeries(CommissionSeriesBase):
    name = 'commission'
    def update_order(self, ticker, size, execute_price, action_type,
                     last_commission,  long_or_short='long'):

        per_comm = self.env.recorder.per_comm
        per_comm_pct = self.env.recorder.per_comm_pct

        if action_type in [ActionType.Buy, ActionType.Short]:

            if per_comm_pct:
                new_value = last_commission + per_comm_pct*size*execute_price
            else:
                new_value = last_commission + per_comm*size/100

            self._append_value(ticker, new_value, long_or_short)


class HoldingPnlSeries(HoldingPnlSeriesBase):
    name = 'holding_pnl'
    def update_order(self, ticker, cur_price, new_avg_price,
                     new_position, long_or_short='long'):

        if new_position == 0:
            new_value = 0
        else:
            earn_short = 1 if long_or_short == 'long' else -1
            new_value = ((cur_price - new_avg_price)*new_position * earn_short)
        self._append_value(ticker, new_value, long_or_short)

    def update_barly(self, order_executed):
        for ticker in self.env.tickers:
            cur_price = self.get_barly_cur_price(ticker, order_executed)

            for long_or_short in ['long', 'short']:
                new_position = self.env.recorder.position.latest(
                    ticker, long_or_short)
                new_avg_price = self.env.recorder.avg_price.latest(
                    ticker, long_or_short)

                self.update_order(ticker, cur_price, new_avg_price,
                                  new_position, long_or_short)


class MarketValueSeries(MarketValueSeriesBase):
    name = 'market_value'
    def update_order(self, ticker,  cur_price, new_position,
                     long_or_short='long'):
        new_value = new_position*cur_price
        self._append_value(ticker,  new_value, long_or_short)

    def update_barly(self, order_executed):
        for ticker in self.env.tickers:
            cur_price = self.get_barly_cur_price(ticker, order_executed)

            for long_or_short in ['long', 'short']:
                new_position = self.env.recorder.position.latest(
                    ticker, long_or_short)
                self.update_order(ticker, cur_price,
                                  new_position, long_or_short)


class MarginSeries(MarginSeriesBase):
    name = 'margin'
    def update_order(self, ticker, long_or_short='long'):

        if long_or_short == 'short':
            new_value = self.env.recorder.market_value.latest(
                ticker, long_or_short)*self.env.recorder.margin_rate
            self._append_value(ticker, new_value, long_or_short)

    def update_barly(self):
        for ticker in self.env.tickers:
            for long_or_short in ['long', 'short']:
                self.update_order(ticker, long_or_short)
