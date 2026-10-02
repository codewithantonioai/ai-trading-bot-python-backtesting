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
          f"{tokens_out:,} out · ${cost:.4f}")


if __name__ == "__main__":
    main()
