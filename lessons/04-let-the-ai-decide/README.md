# Lesson 4 · Let the AI decide

▶ [Watch this lesson](https://youtu.be/LHKgMyiVVzY?t=582) (starts at 9:42)

## Goal

Lesson four. Let the AI decide.

## Commands and files (as shown in the video)

### Terminal · term env

```bash
cat .env.example
echo ".env" >> .gitignore
git status --short --untracked-files=all
```

### Terminal · term add openai

```bash
uv add openai
```

### `ai.py` · vscode decision

```python
import textwrap
from typing import Literal

import pandas as pd
from openai import OpenAI
from pydantic import BaseModel

from data import END, START, TICKER, load_prices

client = OpenAI()
MODEL = "gpt-6-luna"

INSTRUCTIONS = """You are a cautious trading assistant for one anonymous
stock-market ETF. You only see daily data up to today's close.
Decide what to hold tomorrow: BUY (be invested), SELL (be in cash)
or HOLD (keep the current position). Use only the numbers given."""


class Decision(BaseModel):
    action: Literal["BUY", "SELL", "HOLD"]
    confidence: float
    reason: str


def features(history: pd.DataFrame) -> str:
    """The numbers the model is allowed to see: no dates, no name."""
    close = history["Close"]
    returns = close.pct_change()
    last = close.iloc[-1]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1]
    recent = ", ".join(f"{r:+.2%}" for r in returns.iloc[-10:])
    return "\n".join([
        f"5-day return: {close.pct_change(5).iloc[-1]:+.2%}",
        f"20-day return: {close.pct_change(20).iloc[-1]:+.2%}",
        f"vs 20-day average: {last / ma20 - 1:+.2%}",
        f"vs 50-day average: {last / ma50 - 1:+.2%}",
        f"daily volatility: {returns.iloc[-20:].std():.2%}",
        f"last 10 days: {recent}",
    ])


def decide(history: pd.DataFrame, invested: bool):
    position = "invested" if invested else "in cash"
    response = client.responses.parse(
        model=MODEL,
        reasoning={"effort": "low"},
        instructions=INSTRUCTIONS,
        input=f"Position: {position}\n{features(history)}",
        text_format=Decision,
    )
    return response.output_parsed, response.usage


if __name__ == "__main__":
    prices = load_prices(TICKER, START, END)
    print(features(prices))
    decision, usage = decide(prices, invested=False)
    print(f"\n{decision.action} · confidence {decision.confidence:.2f}")
    print(textwrap.fill(decision.reason, 72))
    print(f"{usage.input_tokens} in, {usage.output_tokens} out")
```

### `ai.py` · vscode features

```python
import textwrap
from typing import Literal

import pandas as pd
from openai import OpenAI
from pydantic import BaseModel

from data import END, START, TICKER, load_prices

client = OpenAI()
MODEL = "gpt-6-luna"

INSTRUCTIONS = """You are a cautious trading assistant for one anonymous
stock-market ETF. You only see daily data up to today's close.
Decide what to hold tomorrow: BUY (be invested), SELL (be in cash)
or HOLD (keep the current position). Use only the numbers given."""


class Decision(BaseModel):
    action: Literal["BUY", "SELL", "HOLD"]
    confidence: float
    reason: str


def features(history: pd.DataFrame) -> str:
    """The numbers the model is allowed to see: no dates, no name."""
    close = history["Close"]
    returns = close.pct_change()
    last = close.iloc[-1]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1]
    recent = ", ".join(f"{r:+.2%}" for r in returns.iloc[-10:])
    return "\n".join([
        f"5-day return: {close.pct_change(5).iloc[-1]:+.2%}",
        f"20-day return: {close.pct_change(20).iloc[-1]:+.2%}",
        f"vs 20-day average: {last / ma20 - 1:+.2%}",
        f"vs 50-day average: {last / ma50 - 1:+.2%}",
        f"daily volatility: {returns.iloc[-20:].std():.2%}",
        f"last 10 days: {recent}",
    ])


def decide(history: pd.DataFrame, invested: bool):
    position = "invested" if invested else "in cash"
    response = client.responses.parse(
        model=MODEL,
        reasoning={"effort": "low"},
        instructions=INSTRUCTIONS,
        input=f"Position: {position}\n{features(history)}",
        text_format=Decision,
    )
    return response.output_parsed, response.usage


if __name__ == "__main__":
    prices = load_prices(TICKER, START, END)
    print(features(prices))
    decision, usage = decide(prices, invested=False)
    print(f"\n{decision.action} · confidence {decision.confidence:.2f}")
    print(textwrap.fill(decision.reason, 72))
    print(f"{usage.input_tokens} in, {usage.output_tokens} out")
```

### `ai.py` · vscode decide

```python
import textwrap
from typing import Literal

import pandas as pd
from openai import OpenAI
from pydantic import BaseModel

from data import END, START, TICKER, load_prices

client = OpenAI()
MODEL = "gpt-6-luna"

INSTRUCTIONS = """You are a cautious trading assistant for one anonymous
stock-market ETF. You only see daily data up to today's close.
Decide what to hold tomorrow: BUY (be invested), SELL (be in cash)
or HOLD (keep the current position). Use only the numbers given."""


class Decision(BaseModel):
    action: Literal["BUY", "SELL", "HOLD"]
    confidence: float
    reason: str


def features(history: pd.DataFrame) -> str:
    """The numbers the model is allowed to see: no dates, no name."""
    close = history["Close"]
    returns = close.pct_change()
    last = close.iloc[-1]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1]
    recent = ", ".join(f"{r:+.2%}" for r in returns.iloc[-10:])
    return "\n".join([
        f"5-day return: {close.pct_change(5).iloc[-1]:+.2%}",
        f"20-day return: {close.pct_change(20).iloc[-1]:+.2%}",
        f"vs 20-day average: {last / ma20 - 1:+.2%}",
        f"vs 50-day average: {last / ma50 - 1:+.2%}",
        f"daily volatility: {returns.iloc[-20:].std():.2%}",
        f"last 10 days: {recent}",
    ])


def decide(history: pd.DataFrame, invested: bool):
    position = "invested" if invested else "in cash"
    response = client.responses.parse(
        model=MODEL,
        reasoning={"effort": "low"},
        instructions=INSTRUCTIONS,
        input=f"Position: {position}\n{features(history)}",
        text_format=Decision,
    )
    return response.output_parsed, response.usage


if __name__ == "__main__":
    prices = load_prices(TICKER, START, END)
    print(features(prices))
    decision, usage = decide(prices, invested=False)
    print(f"\n{decision.action} · confidence {decision.confidence:.2f}")
    print(textwrap.fill(decision.reason, 72))
    print(f"{usage.input_tokens} in, {usage.output_tokens} out")
```

### Terminal · term decide

```bash
uv run --env-file .env ai.py
```

## Recap

So: the model gets numbers, never dates or names. It answers BUY, SELL or HOLD with a reason. And Pydantic validates every answer. One decision works. Now let's make eighty five of them, without cheating.
