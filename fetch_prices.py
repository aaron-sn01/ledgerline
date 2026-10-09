"""Ledgerline price updater.

Reads the funds in tickers.json and funds.txt (an ISIN is enough; the symbol is found), downloads about 400 days of
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
config = None


def all_funds():
    """The funds to fetch: tickers.json plus the simple list in funds.txt (one ISIN per line, optional name)."""
    out = list(json.loads((ROOT / "tickers.json").read_text())["tickers"])
    known = {t.get("isin") for t in out}
    try:
        for line in (ROOT / "funds.txt").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            isin, _, name = line.partition(" ")
            isin = isin.strip().upper()
            if len(isin) == 12 and isin not in known:
                out.append({"isin": isin, "name": name.strip() or isin})
                known.add(isin)
    except FileNotFoundError:
        pass
    return out


def find_symbol(isin, found):
    """Yahoo symbol for an ISIN: remembered from earlier runs, otherwise searched (Xetra preferred)."""
    if found.get(isin):
        return found[isin]
    try:
        hits = [q.get("symbol") for q in (yf.Search(isin, max_results=10).quotes or []) if q.get("symbol")]
    except Exception:
        hits = []
    for suffix in (".DE", ".F", ".AS", ".PA", ".MI", ".L", ""):
        for h in hits:
            if h.endswith(suffix) if suffix else True:
                return h
    return None


try:
    _prev = json.loads((ROOT / "prices.json").read_text())
except (FileNotFoundError, json.JSONDecodeError):
    _prev = {}
previous, found = _prev.get("quotes", {}), dict(_prev.get("found", {}))
funds = all_funds()

quotes, errors = {}, []
for entry in funds:
    symbol = entry.get("symbol") or find_symbol(entry["isin"], found)
    if not symbol:
        errors.append(f"{entry['isin']}: no price symbol found for this ISIN")
        continue
    if not entry.get("symbol"):
        found[entry["isin"]] = symbol
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
    "found": found,
}
(ROOT / "prices.json").write_text(json.dumps(out, separators=(",", ":")))
print(f"{len(quotes)} of {len(funds)} funds written")
for e in errors:
    print("  problem:", e)
