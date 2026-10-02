import pandas as pd
from backtesting import Strategy

from data import TEST_START


def SMA(values, n):
    """Simple moving average of the last n closes."""
    return pd.Series(values).rolling(n).mean()


class BuyAndHold(Strategy):
    def init(self):
        pass

    def next(self):
        today = self.data.index[-1]
        if today >= pd.Timestamp(TEST_START) and not self.position:
            self.buy()


class SmaTrend(Strategy):
    fast, slow = 10, 20  # the values from the Backtesting.py example

    def init(self):
        self.fast_ma = self.I(SMA, self.data.Close, self.fast)
        self.slow_ma = self.I(SMA, self.data.Close, self.slow)

    def next(self):
        if self.data.index[-1] < pd.Timestamp(TEST_START):
            return
        uptrend = self.fast_ma[-1] > self.slow_ma[-1]
        if uptrend and not self.position:
            self.buy()
        elif not uptrend and self.position:
            self.position.close()
