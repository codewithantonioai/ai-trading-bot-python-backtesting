# Lesson 7 · Read the results honestly

▶ [Watch this lesson](https://youtu.be/LHKgMyiVVzY?t=1161) (starts at 19:21)

## Goal

Lesson seven. Read the results honestly.

## Commands and files (as shown in the video)

### Terminal · term qqq

```bash
sed -i 's/TICKER = "SPY"/TICKER = "QQQ"/' data.py
grep TICKER data.py | head -1
uv run --env-file .env signals.py | tail -3
uv run backtest.py
```

## Recap

So: tuning a strategy, or a prompt, until it wins is overfitting. On two markets, the AI came last. And the honest next step is fresh data and paper trading, not real money.
