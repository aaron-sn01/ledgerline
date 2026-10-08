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
UA = {"User-Agent": "Mozilla/5.0 (Ledgerline composition updater)"}

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


def ishares(src):
    url = (f"https://www.ishares.com/uk/individual/en/products/{src['productId']}/{src['slug']}/"
           f"1506575576011.ajax?fileType=csv&fileName={src['ticker']}_holdings&dataType=fund")
    text = fetch(url).decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if "Weight (%)" in l and "Location" in l), None)
    if start is None:
        raise ValueError("no holdings table in the download (the provider may have changed or blocked the file)")
    rows = csv.DictReader(io.StringIO("\n".join(lines[start:])))
    sectors, countries = {}, {}
    for row in rows:
        if not row.get("Name") or row.get("Weight (%)") in (None, "", "-"):
            continue
        if (row.get("Asset Class") or "Equity").strip().lower() != "equity":
            continue
        sector = (row.get("Sector") or "Other").strip()
        if any(s in sector.lower() for s in SKIP):
            continue
        try:
            w = float(row["Weight (%)"].replace(",", ""))
        except ValueError:
            continue
        if math.isnan(w):
            continue
        loc = (row.get("Location") or "Other").strip()
        sectors[SECTOR.get(sector, sector)] = sectors.get(SECTOR.get(sector, sector), 0) + w
        countries[COUNTRY.get(loc, loc)] = countries.get(COUNTRY.get(loc, loc), 0) + w
    return norm(sectors), norm(countries), url


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

funds, errors = dict(previous), []
today = dt.date.today().isoformat()
for t in json.loads((ROOT / "tickers.json").read_text())["tickers"]:
    src, isin = t.get("composition"), t.get("isin")
    if not src or not isin:
        continue
    try:
        if src["provider"] == "ishares":
            sectors, countries, url = ishares(src)
        elif src["provider"] == "dws":
            sectors, countries, url = dws(isin)
        else:
            continue
        funds[isin] = {"asOf": today, "source": src["provider"], "sectors": sectors, "countries": countries}
    except Exception as exc:  # keep last month's numbers if a provider changes its file
        errors.append(f"{t['symbol']}: {exc or type(exc).__name__}")

out = {"updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "funds": funds, "errors": errors}
(ROOT / "compositions.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print(f"{len(funds)} funds in compositions.json")
for e in errors:
    print("  problem:", e)
