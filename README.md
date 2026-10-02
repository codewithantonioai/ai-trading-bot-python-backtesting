# Build an AI Trading Bot with Python (Backtesting, No Real Money)

Companion repository for the **Code with Antonio** video course · [Watch on YouTube](https://youtu.be/LHKgMyiVVzY).

Build an AI trading bot with Python and backtest it with no real money: yfinance data, a classic strategy and GPT-6 Luna.

## What you'll build

A bot that downloads real S&P 500 prices, tests a classic moving-average strategy, asks GPT-6 Luna every day whether to buy, sell or hold, and puts both against buy & hold in an honest backtest with $10,000 of fake money.

## Lessons

| # | Lesson | Video | Folder |
|---|---|---|---|
| 1 | What is an AI trading bot? | [0:00](https://youtu.be/LHKgMyiVVzY?t=0) | [lessons/01-what-is-an-ai-trading-bot](lessons/01-what-is-an-ai-trading-bot) |
| 2 | Real market data with yfinance | [3:00](https://youtu.be/LHKgMyiVVzY?t=180) | [lessons/02-real-market-data-with-yfinance](lessons/02-real-market-data-with-yfinance) |
| 3 | A classic strategy and your first backtest | [6:01](https://youtu.be/LHKgMyiVVzY?t=361) | [lessons/03-a-classic-strategy-and-your-first-backtest](lessons/03-a-classic-strategy-and-your-first-backtest) |
| 4 | Let the AI decide | [9:42](https://youtu.be/LHKgMyiVVzY?t=582) | [lessons/04-let-the-ai-decide](lessons/04-let-the-ai-decide) |
| 5 | Don't let the AI cheat | [13:29](https://youtu.be/LHKgMyiVVzY?t=809) | [lessons/05-don-t-let-the-ai-cheat](lessons/05-don-t-let-the-ai-cheat) |
| 6 | AI vs. the classics: the backtest | [17:02](https://youtu.be/LHKgMyiVVzY?t=1022) | [lessons/06-ai-vs-the-classics-the-backtest](lessons/06-ai-vs-the-classics-the-backtest) |
| 7 | Read the results honestly | [19:21](https://youtu.be/LHKgMyiVVzY?t=1161) | [lessons/07-read-the-results-honestly](lessons/07-read-the-results-honestly) |

## Requirements

- Python 3.14 · uv 0.12.21 · yfinance 1.7.0 · Backtesting.py 0.6.6 · pandas 3.0.6 · openai 3.22.1 · gpt-6-luna · Ubuntu (Linux)
- Python 3.12+ and [uv](https://docs.astral.sh/uv/)

## Run the final project

```bash
cd app
uv sync
uv run data.py
uv run backtest.py
cp .env.example .env   # add your OPENAI_API_KEY
uv run --env-file .env signals.py
```

## Repository structure

```
README.md          this file
lessons/           one folder per lesson: goal, timestamp, commands and files exactly as in the video
app/               the final working project
assets/            thumbnail
```

## License

MIT — use it for anything, credit appreciated.

---
Generated on 2026-10-02 from the course scripts. Code with Antonio · AI tutor.