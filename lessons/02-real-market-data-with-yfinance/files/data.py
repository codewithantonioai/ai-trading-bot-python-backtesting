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
