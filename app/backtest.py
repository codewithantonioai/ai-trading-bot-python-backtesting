import json
from pathlib import Path

import pandas as pd
from backtesting import Backtest, Strategy

from data import DECISIONS, END, START, TEST_START, TICKER, load_prices
from strategy import BuyAndHold, SmaTrend


class AiStrategy(Strategy):
    def init(self):
        self.decisions = json.loads(DECISIONS.read_text())

    def next(self):
        day = f"{self.data.index[-1]:%Y-%m-%d}"
        action = self.decisions.get(day, {}).get("action")
        if action == "BUY" and not self.position:
            self.buy()
        elif action == "SELL" and self.position:
            self.position.close()


STRATEGIES = {
    "Buy & hold": BuyAndHold,
    "SMA 10/20": SmaTrend,
    "AI (gpt-6-luna)": AiStrategy,
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
