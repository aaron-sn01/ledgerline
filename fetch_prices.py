"""Ledgerline price updater.

Reads the funds in tickers.json and funds.txt (an ISIN is enough; the symbol is found), downloads about 400 days of
daily closing prices for each, and writes prices.json next to the app.
It also keeps price-history.json: every daily close back to 2010 for each fund, and for the coins listed in funds.txt
(a line like "ETH Ethereum"). The long history is downloaded once per fund or coin; after that each run only adds the
new days. The app loads it only for investment returns and the wealth history.
Runs on GitHub Actions; no personal data is involved. If a symbol fails,
its previous prices are kept so the app never loses a price.
"""
import datetime as dt
import json
import pathlib
import re
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


# Coinbase's names for a few coins, and coins that became another one
COIN_ALIAS = {"CGLD": "CELO", "ETH2": "ETH"}


def all_coins():
    """Coins listed in funds.txt: a short symbol instead of an ISIN, e.g. "ETH Ethereum" or "XLM Stellar"."""
    out, seen = [], set()
    try:
        for line in (ROOT / "funds.txt").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            sym, _, name = line.partition(" ")
            sym = COIN_ALIAS.get(sym.strip().upper(), sym.strip().upper())
            if len(sym) != 12 and re.fullmatch(r"[A-Z0-9]{2,10}", sym) and sym not in seen:
                out.append({"symbol": sym, "name": name.strip() or sym})
                seen.add(sym)
    except FileNotFoundError:
        pass
    return out


def sig(v):
    """A close rounded to 6 significant digits: exact enough for any price, from 0.0001 to 100000."""
    return float(f"{float(v):.6g}")


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
try:
    _hist = json.loads((ROOT / "price-history.json").read_text())
except (FileNotFoundError, json.JSONDecodeError):
    _hist = {}
HIST_FROM = "2010-01-01"
hist_out = {"quotes": {}, "crypto": {}}


def long_history(tk, symbol, kind, recent, factor=1.0):
    """Every close back to 2010: the stored one plus the recent days; downloaded in full only the first time
    (or until a full download worked). Returns (closes, full)."""
    old = (_hist.get(kind) or {}).get(symbol) or {}
    closes, full = dict(old.get("history") or {}), bool(old.get("full"))
    if not full:
        try:
            h = tk.history(start=HIST_FROM, interval="1d", auto_adjust=False, timeout=30).dropna(subset=["Close"])
            if not h.empty:
                closes.update({d.strftime("%Y-%m-%d"): sig(float(c) * factor) for d, c in h["Close"].items()})
                full = True
        except Exception as exc:
            errors.append(f"{symbol}: long history not downloaded yet ({exc})")
    closes.update({d: sig(v) for d, v in recent.items()})
    return dict(sorted(closes.items())), full

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
            pence = currency in ("GBp", "GBX")
            if pence:
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
            lh, full = long_history(tk, symbol, "quotes", closes, 0.01 if pence else 1.0)
            hist_out["quotes"][symbol] = {"isin": entry.get("isin"), "name": entry.get("name"), "currency": currency.upper(), "full": full, "history": lh}
            break
        except Exception as exc:  # network hiccups, rate limits, unknown symbols
            if attempt == 2:
                errors.append(f"{symbol}: {exc}")
                if symbol in previous:
                    quotes[symbol] = previous[symbol]
                if symbol in (_hist.get("quotes") or {}):
                    hist_out["quotes"][symbol] = _hist["quotes"][symbol]
            else:
                time.sleep(5 * (attempt + 1))
    time.sleep(1)

# Coins: daily closes in euros (Yahoo's "ETH-EUR"), for the returns and the wealth history; live coin prices still come from CoinGecko
coins = all_coins()
for c in coins:
    ysym = f"{c['symbol']}-EUR"
    try:
        tk = yf.Ticker(ysym)
        h = tk.history(period="1mo", interval="1d", auto_adjust=False, timeout=20).dropna(subset=["Close"])
        recent = {d.strftime("%Y-%m-%d"): float(v) for d, v in h["Close"].items()}
        if not recent:
            raise ValueError("no data returned")
        lh, full = long_history(tk, c["symbol"], "crypto", recent)
        hist_out["crypto"][c["symbol"]] = {"name": c["name"], "currency": "EUR", "full": full, "history": lh}
    except Exception as exc:
        errors.append(f"{ysym}: {exc}")
        if c["symbol"] in (_hist.get("crypto") or {}):
            hist_out["crypto"][c["symbol"]] = _hist["crypto"][c["symbol"]]
    time.sleep(1)

out = {
    "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    "quotes": quotes,
    "errors": errors,
    "found": found,
}
(ROOT / "prices.json").write_text(json.dumps(out, separators=(",", ":")))
hist_out = {"updated": out["updated"], **hist_out}
(ROOT / "price-history.json").write_text(json.dumps(hist_out, separators=(",", ":")))
print(f"{len(quotes)} of {len(funds)} funds written; history for {len(hist_out['quotes'])} funds and {len(hist_out['crypto'])} coins")
for e in errors:
    print("  problem:", e)
