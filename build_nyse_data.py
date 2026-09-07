import csv, sys, io, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SRC = r"H:\קלוד\הורדות\NYSE3.csv"
OUT = r"H:\קלוד\קלוד 2\nyse_data.tsv"

def parse_price(p):
    p = p.strip()
    if not p:
        return None
    if p.endswith("K"):
        try:
            return round(float(p[:-1]) * 1000, 2)
        except ValueError:
            return None
    try:
        return round(float(p), 2)
    except ValueError:
        return None

rows = []
k_notation_tickers = []
seen = set()
dupes = []

with open(SRC, encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if len(row) < 7:
            continue
        _img, ticker, name, price_raw, cons, rating, div = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        ticker = ticker.strip()
        name = name.strip()
        if not ticker:
            continue
        if ticker in seen:
            dupes.append(ticker)
            continue
        seen.add(ticker)
        price = parse_price(price_raw)
        if price is None:
            print(f"WARN: could not parse price for {ticker}: {price_raw!r}", file=sys.stderr)
            price = 0.0
        if price_raw.strip().endswith("K"):
            k_notation_tickers.append((ticker, price_raw, price))
        cons = cons.strip()
        rating = rating.strip()
        div = div.strip()
        rows.append((ticker, name, f"{price:.2f}", cons, rating, div))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    for r in rows:
        f.write("\t".join(r) + "\n")

print(f"Wrote {len(rows)} tickers to {OUT}")
print(f"Duplicate tickers skipped: {len(dupes)}: {dupes}")
print(f"K-notation prices converted ({len(k_notation_tickers)}): approximate, need precise re-check during per-letter pass:")
for t, raw, val in k_notation_tickers:
    print(f"  {t}: {raw} -> {val}")
