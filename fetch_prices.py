"""Ledgerline price updater.

Reads the Yahoo Finance symbols in tickers.json, downloads about 400 days of
daily closing prices for each, and writes prices.json next to the app.
Runs on GitHub Actions; no personal data is involved. If a symbol fails,
its previous prices are kept so the app never loses a price.
"""
import datetime as dt
import json
import pathlib
import time

import yfinance as yf

ROOT = pathlib.Path(__file__).resolve().parent
config = json.loads((ROOT / "tickers.json").read_text())

try:
    previous = json.loads((ROOT / "prices.json").read_text()).get("quotes", {})
except (FileNotFoundError, json.JSONDecodeError):
    previous = {}

quotes, errors = {}, []
for entry in config["tickers"]:
    symbol = entry["symbol"]
    for attempt in range(3):
        try:
            tk = yf.Ticker(symbol)
            hist = tk.history(period="400d", interval="1d", auto_adjust=False, timeout=20)
            hist = hist.dropna(subset=["Close"])
            if hist.empty:
                raise ValueError("no data returned")
            closes = {d.strftime("%Y-%m-%d"): round(float(c), 4) for d, c in hist["Close"].items()}
            # The currency the price is quoted in. London lines quote in pence ("GBp"): convert to pounds.
            try:
                currency = (tk.fast_info.get("currency") or entry.get("currency") or "EUR")
            except Exception:
                currency = entry.get("currency") or "EUR"
            if currency in ("GBp", "GBX"):
                closes = {d: round(v / 100, 4) for d, v in closes.items()}
                currency = "GBP"
            days = sorted(closes)
            quotes[symbol] = {
                "isin": entry.get("isin"),
                "name": entry.get("name"),
                "price": closes[days[-1]],
                "prevClose": closes[days[-2]] if len(days) > 1 else closes[days[-1]],
                "date": days[-1],
                "currency": currency.upper(),
                "history": closes,
            }
            break
        except Exception as exc:  # network hiccups, rate limits, unknown symbols
            if attempt == 2:
                errors.append(f"{symbol}: {exc}")
                if symbol in previous:
                    quotes[symbol] = previous[symbol]
            else:
                time.sleep(5 * (attempt + 1))
    time.sleep(1)

out = {
    "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    "quotes": quotes,
    "errors": errors,
}
(ROOT / "prices.json").write_text(json.dumps(out, separators=(",", ":")))
print(f"{len(quotes)} of {len(config['tickers'])} symbols written")
for e in errors:
    print("  problem:", e)
