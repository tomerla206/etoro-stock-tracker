import glob
import re

ROWS_FILE = "all_rows.html"

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def load_targets():
    targets = {}
    skipped = 0
    files = sorted(f for f in glob.glob("analyst_targets_*.txt") if "_OLD" not in f)
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                fields = line.split("\t")
                if len(fields) == 8:
                    ticker, name, price, low, avg, high, status, trade = fields
                elif len(fields) == 7:
                    if is_number(fields[3]):
                        # AnalysisStatus column was dropped entirely; low/avg/high
                        # are real numeric values, not blank placeholders.
                        ticker, name, price, low, avg, high, trade = fields
                        status = "OK" if (low or avg or high) else "NOFAQ"
                    else:
                        # Legacy/typo NOFAQ shape: field 3/4 hold blank or a
                        # repeated "NOFAQ" placeholder, real status is field 5.
                        ticker, name, price, _, _, status, trade = fields
                        low = avg = high = ""
                else:
                    skipped += 1
                    continue
                if status == "MISMATCH":
                    skipped += 1
                    continue
                targets[ticker] = {
                    "price": price, "low": low, "avg": avg, "high": high,
                    "status": status, "trade": trade,
                }
    print(f"Loaded {len(targets)} valid ticker records (after skipping {skipped} MISMATCH/malformed) from analyst_targets_*.txt")
    return targets

def cell(cls, value):
    if value:
        return f'<td class="{cls} col-target">{value}</td>'
    return f'<td class="{cls} col-target empty">&ndash;</td>'

def patch_row(line, t):
    line = re.sub(r'data-price="[^"]*"', f'data-price="{t["price"]}"', line, count=1)
    line = re.sub(r'data-low="[^"]*"', f'data-low="{t["low"]}"', line, count=1)
    line = re.sub(r'data-avg="[^"]*"', f'data-avg="{t["avg"]}"', line, count=1)
    line = re.sub(r'data-high="[^"]*"', f'data-high="{t["high"]}"', line, count=1)

    if t["trade"] == "NOT_TRADEABLE":
        new_class = ' class="row-not-tradeable"'
    elif t["status"] == "NOFAQ":
        new_class = ' class="row-nofaq"'
    else:
        new_class = ""
    # Only touch the <tr ...> opening tag's own attributes/class, never
    # anything inside the row (td/span elements also have class="...">).
    m = re.match(r'^(\s*<tr\b[^>]*)>', line)
    if not m:
        raise ValueError(f"Could not parse <tr> opening tag in line: {line!r}")
    prefix = re.sub(r'\s+class="[^"]*"', "", m.group(1))
    line = prefix + new_class + ">" + line[m.end():]

    line = re.sub(r'<td class="price">[^<]*</td>', f'<td class="price">{t["price"]}</td>', line, count=1)
    line = re.sub(r'<td class="analysis-cell analysis-low[^"]*">[^<]*</td>', cell("analysis-cell analysis-low", t["low"]), line, count=1)
    line = re.sub(r'<td class="analysis-cell analysis-avg[^"]*">[^<]*</td>', cell("analysis-cell analysis-avg", t["avg"]), line, count=1)
    line = re.sub(r'<td class="analysis-cell analysis-high[^"]*">[^<]*</td>', cell("analysis-cell analysis-high", t["high"]), line, count=1)
    return line

def main():
    targets = load_targets()
    with open(ROWS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    ticker_re = re.compile(r'data-ticker="([^"]+)"')
    updated = 0
    matched_tickers = set()
    out_lines = []
    for line in lines:
        m = ticker_re.search(line)
        if m:
            ticker = m.group(1)
            if ticker in targets:
                line = patch_row(line, targets[ticker])
                updated += 1
                matched_tickers.add(ticker)
        out_lines.append(line)

    unmatched = sorted(set(targets) - matched_tickers)
    if unmatched:
        print(f"WARNING: {len(unmatched)} tickers from analyst_targets files had no matching row in {ROWS_FILE}: {unmatched}")

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.writelines(out_lines)
    print(f"Updated {updated} rows in {ROWS_FILE}")

if __name__ == "__main__":
    main()
