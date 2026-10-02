# Lesson 5 · Don't let the AI cheat

▶ [Watch this lesson](https://youtu.be/LHKgMyiVVzY?t=809) (starts at 13:29)

## Goal

Lesson five. Don't let the AI cheat.

## Commands and files (as shown in the video)

### `data.py` · vscode data l5

```python
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKER = "SPY"
START, END = "2025-01-01", "2026-10-01"
TEST_START = "2026-06-01"  # after the model's knowledge cutoff
DATA_DIR = Path("data")
DECISIONS = Path(f"decisions-{TICKER}.json")


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

### `signals.py` · vscode signals

```python
import json

from ai import decide
from data import DECISIONS, END, START, TEST_START, TICKER, load_prices


def main():
    prices = load_prices(TICKER, START, END)
    cache = json.loads(DECISIONS.read_text()) if DECISIONS.exists() else {}
    invested = False

    for day in prices.loc[TEST_START:].index:
        key = f"{day:%Y-%m-%d}"
        if key not in cache:
            history = prices.loc[:day]  # only what we knew at that close
            decision, usage = decide(history, invested)
            cache[key] = decision.model_dump() | {
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
            }
            DECISIONS.write_text(json.dumps(cache, indent=2))

        d = cache[key]
        if d["action"] != "HOLD":
            invested = d["action"] == "BUY"
        print(f"{key}  {d['action']:<4}  {d['confidence']:.2f}  {d['reason'][:58]}",
              flush=True)

    tokens_in = sum(d["input_tokens"] for d in cache.values())
    tokens_out = sum(d["output_tokens"] for d in cache.values())
    cost = tokens_in * 0.10 / 1e6 + tokens_out * 0.50 / 1e6
    print(f"\n{len(cache)} decisions · {tokens_in:,} tokens in · "
          f"{tokens_out:,} out · \${cost:.4f}")


if __name__ == "__main__":
    main()
```

### Terminal · term signals start

```bash
uv run --env-file .env signals.py
```

### Terminal · term cached

```bash
time uv run --env-file .env signals.py | tail -4
head -9 decisions-SPY.json
```

## Recap

So: we cut the history at each day's close, and orders fill the next morning. The AI only trades days after its knowledge cutoff. And we ask once and cache every answer. Now, the moment of truth.
