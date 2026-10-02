# Lesson 3 · A classic strategy and your first backtest

▶ [Watch this lesson](https://youtu.be/LHKgMyiVVzY?t=361) (starts at 6:01)

## Goal

Lesson three. A classic strategy, and your first backtest.

## Commands and files (as shown in the video)

### `strategy.py` · vscode strategy

```python
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
```

### Terminal · term add backtesting

```bash
uv add backtesting
```

### `backtest.py` · vscode backtest

```python
from pathlib import Path

import pandas as pd
from backtesting import Backtest

from data import END, START, TEST_START, TICKER, load_prices
from strategy import BuyAndHold, SmaTrend


STRATEGIES = {
    "Buy & hold": BuyAndHold,
    "SMA 10/20": SmaTrend,
}
METRICS = ["Return [%]", "Max. Drawdown [%]", "# Trades",
           "Win Rate [%]", "Commissions [$]"]


def main():
    prices = load_prices(TICKER, START, END)
    Path("reports").mkdir(exist_ok=True)
    results = {}
    for name, strategy in STRATEGIES.items():
        bt = Backtest(prices, strategy, cash=10_000, commission=0.002,
                      finalize_trades=True)
        stats = bt.run()
        results[name] = stats[METRICS]
        bt.plot(filename=f"reports/{TICKER}-{strategy.__name__}.html",
                open_browser=False)

    print(f"{TICKER} · {TEST_START} → {prices.index[-1]:%Y-%m-%d} · "
          "$10,000 · 0.2% commission\n")
    print(pd.DataFrame(results).T.astype(float).round(2).to_string())


if __name__ == "__main__":
    main()
```

### Terminal · term backtest

```bash
uv run backtest.py
```

## Recap

So: our classic rule is invested when the fast average is above the slow one. Orders fill at the next open, never at a price we already saw. And the classic strategy lost to buy and hold. Can an AI do better? Let's find out.
