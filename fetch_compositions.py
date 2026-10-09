import math
"""Ledgerline composition updater.

Once a month, downloads the full holdings list each fund provider publishes,
and turns it into sector and country weights per ETF (compositions.json).
iShares and Xtrackers publish machine-readable holdings files; for funds
without one, the previous values are kept. Nothing personal is involved.
"""
import csv
import datetime as dt
import io
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
      "Accept": "text/csv,application/vnd.ms-excel,text/plain,*/*;q=0.8", "Accept-Language": "en-GB,en;q=0.9,de;q=0.8"}

COUNTRY = {
    "United States of America": "United States", "USA": "United States", "Korea (South)": "South Korea",
    "Korea, Republic of": "South Korea", "Republic of Korea": "South Korea", "Korea": "South Korea",
    "Taiwan, Province of China": "Taiwan", "China (Mainland)": "China", "Hong Kong SAR": "Hong Kong",
    "United Arab Emirates": "UAE", "Russian Federation": "Russia", "Czechia": "Czech Republic",
    "Türkiye": "Turkey", "Great Britain": "United Kingdom", "UK": "United Kingdom",
}
SECTOR = {
    "Communication": "Communication services", "Communication Services": "Communication services",
    "Telecommunication Services": "Communication services", "Information Technology": "Information technology",
    "Health Care": "Health care", "Consumer Discretionary": "Consumer discretionary", "Consumer Staples": "Consumer staples",
    "Real Estate": "Real estate",
}
SKIP = ("cash", "derivative", "futures", "fx", "money market")


def norm(weights):
    weights = {k: v for k, v in weights.items() if not math.isnan(v)}
    total = sum(weights.values())
    if not weights:
        raise ValueError("no weights found in the download")
    if not 80 <= total <= 120 and not 0.8 <= total <= 1.2:
        raise ValueError(f"weights add up to {total:.1f}, which looks wrong")
    return {k: round(v * 100 / total, 2) for k, v in sorted(weights.items(), key=lambda kv: -kv[1]) if v > 0}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


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


# iShares blocks automatic downloads from GitHub's servers (it sends a web page instead of the file, seen 08/10/2026).
# Their funds are updated in the app instead: download the holdings list on the iShares website and import it.
ISHARES_AUTO = False


def ishares(src):
    """Tries the UK and German iShares sites; says plainly when iShares sends a web page instead of the file."""
    pid, slug, tick = src["productId"], src["slug"], src["ticker"]
    urls = [f"https://www.ishares.com/uk/individual/en/products/{pid}/{slug}/1506575576011.ajax?fileType=csv&fileName={tick}_holdings&dataType=fund",
            f"https://www.ishares.com/uk/professional/en/products/{pid}/{slug}/1506575576011.ajax?fileType=csv&fileName={tick}_holdings&dataType=fund",
            f"https://www.ishares.com/de/privatanleger/de/produkte/{pid}/{slug}/1478358465952.ajax?fileType=csv&fileName={tick}_holdings&dataType=fund"]
    seen = []
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={**UA, "Referer": url.split("/1506575576011")[0].split("/1478358465952")[0]})
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode("utf-8-sig", errors="replace")
        except Exception as exc:
            seen.append(f"{exc.__class__.__name__}: {exc}"); continue
        if text.lstrip()[:1] == "<":
            seen.append("got a web page instead of the file (iShares probably blocks automatic downloads)"); continue
        lines = text.splitlines()
        start = next((i for i, l in enumerate(lines) if ("Weight (%)" in l or "Gewichtung (%)" in l) and ("Location" in l or "Standort" in l)), None)
        if start is None:
            seen.append("no holdings table in the download (the provider may have changed the file)"); continue
        rows = csv.DictReader(io.StringIO("\n".join(lines[start:])))
        sectors, countries = {}, {}
        for row in rows:
            name, wraw = row.get("Name"), row.get("Weight (%)") or row.get("Gewichtung (%)")
            if not name or wraw in (None, "", "-"):
                continue
            if (row.get("Asset Class") or row.get("Anlageklasse") or "Equity").strip().lower() not in ("equity", "aktien"):
                continue
            sector = (row.get("Sector") or row.get("Sektor") or "Other").strip()
            if any(x in sector.lower() for x in SKIP):
                continue
            try:
                w = float(wraw.replace(",", ".") if "," in wraw and "." not in wraw else wraw.replace(",", ""))
            except ValueError:
                continue
            if math.isnan(w):
                continue
            loc = (row.get("Location") or row.get("Standort") or "Other").strip()
            sectors[SECTOR.get(sector, sector)] = sectors.get(SECTOR.get(sector, sector), 0) + w
            countries[COUNTRY.get(loc, loc)] = countries.get(COUNTRY.get(loc, loc), 0) + w
        if sectors:
            return norm(sectors), norm(countries), url
        seen.append("the download had no equity rows")
    raise ValueError(seen[-1] if seen else "no data received")


def dws(isin):
    import pandas as pd
    url = f"https://etf.dws.com/etfdata/export/GBR/ENG/excel/product/constituent/{isin}/"
    raw = pd.read_excel(io.BytesIO(fetch(url)), header=None)
    head = next(i for i, r in raw.iterrows() if any(str(c).strip() in ("Weighting", "Weight") for c in r.values))
    df = raw.iloc[head + 1:].copy()
    df.columns = [str(c).strip() for c in raw.iloc[head].values]
    wcol = "Weighting" if "Weighting" in df.columns else "Weight"
    scol = next(c for c in df.columns if c in ("Industry Classification", "Sector", "Industry"))
    tcol = next((c for c in df.columns if c in ("Type of Security", "Asset Class")), None)
    sectors, countries = {}, {}
    for _, r in df.iterrows():
        try:
            w = float(str(r[wcol]).replace("%", "").replace(",", ""))
        except ValueError:
            continue
        if math.isnan(w):
            continue
        if tcol and "equit" not in str(r[tcol]).lower() and "share" not in str(r[tcol]).lower():
            continue
        sector = str(r[scol]).strip()
        if not sector or sector == "nan" or any(s in sector.lower() for s in SKIP):
            continue
        loc = str(r.get("Country", "Other")).strip()
        sectors[SECTOR.get(sector, sector)] = sectors.get(SECTOR.get(sector, sector), 0) + w
        countries[COUNTRY.get(loc, loc)] = countries.get(COUNTRY.get(loc, loc), 0) + w
    return norm(sectors), norm(countries), url


try:
    previous = json.loads((ROOT / "compositions.json").read_text()).get("funds", {})
except (FileNotFoundError, json.JSONDecodeError):
    previous = {}

funds, errors, manual = dict(previous), [], []
today = dt.date.today().isoformat()
try:
    names = {q.get("isin"): q.get("name") for q in json.loads((ROOT / "prices.json").read_text()).get("quotes", {}).values()}
except (FileNotFoundError, json.JSONDecodeError):
    names = {}
for t in all_funds():
    src, isin = t.get("composition"), t.get("isin")
    if not isin:
        continue
    if not src:   # a fund from funds.txt: the provider is recognised from its name
        nm = f"{t.get('name') or ''} {names.get(isin) or ''}"
        if "xtrackers" in nm.lower():
            src = {"provider": "dws"}
        elif "ishares" in nm.lower():
            q = f"https://www.google.com/search?q={isin}+site%3Aishares.com"
            manual.append({"isin": isin, "symbol": t.get("symbol") or isin, "name": (t.get("name") if t.get("name") != isin else None) or names.get(isin) or isin, "en": q, "de": q})
            continue
        else:
            continue
    try:
        if src["provider"] == "ishares":
            if not ISHARES_AUTO:
                print(f"  {t['symbol']}: iShares, updated in the app by importing its holdings list")
                manual.append({"isin": isin, "symbol": t["symbol"], "name": t.get("name", t["symbol"]),
                               "en": f"https://www.ishares.com/uk/individual/en/products/{src['productId']}/{src['slug']}",
                               "de": f"https://www.ishares.com/de/privatanleger/de/produkte/{src['productId']}/{src['slug']}"})
                continue
            sectors, countries, url = ishares(src)
        elif src["provider"] == "dws":
            sectors, countries, url = dws(isin)
        else:
            continue
        funds[isin] = {"asOf": today, "source": src["provider"], "sectors": sectors, "countries": countries}
    except Exception as exc:  # keep last month's numbers if a provider changes its file
        errors.append(f"{t['symbol']}: {exc or type(exc).__name__}")

out = {"updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "funds": funds, "errors": errors, "manual": manual}
(ROOT / "compositions.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print(f"{len(funds)} funds in compositions.json")
for e in errors:
    print("  problem:", e)
