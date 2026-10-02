# Lesson 2 · Real market data with yfinance

▶ [Watch this lesson](https://youtu.be/LHKgMyiVVzY?t=180) (starts at 3:00)

## Goal

Lesson two. Real market data with yfinance.

## Commands and files (as shown in the video)

### Terminal · term uv init

```bash
uv init --no-package tradebot
cd tradebot
ls -a
```

### Terminal · term uv add

```bash
uv add yfinance
```

### `data.py` · vscode data

```python
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKER = "SPY"
START, END = "2025-01-01", "2026-10-01"
DATA_DIR = Path("data")


def load_prices(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Daily prices from Yahoo Finance, cached as a CSV file."""
    path = DATA_DIR / f"{ticker}_{start}_{end}.csv"
    if path.exists():
        return pd.read_csv(path, index_col="Date", parse_dates=True)

    df = yf.download(ticker, start=start, end=end, auto_adjust=True,
                     progress=False, multi_level_index=False)
    DATA_DIR.mkdir(exist_ok=True)
    df.round(2).to_csv(path)
    return df.round(2)


if __name__ == "__main__":
    prices = load_prices(TICKER, START, END)
    print(prices.head(3))
    print(prices.tail(3))
    print(f"{len(prices)} trading days of {TICKER}")
```

### Terminal · term data

```bash
uv run data.py
```

### Terminal · term cache

```bash
time uv run data.py
```

## Recap

So: a uv project with plain scripts. One row per trading day, with open, high, low, close and volume. And we download once, then read the CSV. Now let's give these prices a strategy.
