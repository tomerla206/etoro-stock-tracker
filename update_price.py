"""
UPDATE PRICE - refreshes the Price column using the fresh Yahoo close price
that fundamentals_scan.py already fetches (for its own RSI/MA calculations)
but never wrote back to the visible Price column.

Price was previously static forever: no scan actually refreshed the price
field in analyst_targets_*.txt (MEGASCAN/SCAN VALUES only touch Low/Avg/High
and pass price through unchanged; merge_analyst_targets.py just round-trips
whatever's already in the file). This closes that gap using data that's
already being fetched anyway - no new network calls.

Run AFTER fundamentals_scan.py has produced a fresh fundamentals_data.tsv.
Writes the new price into analyst_targets_*.txt (same files MEGASCAN
maintains) - a raw data file only, same as every other scan's output. Does
NOT merge into all_rows.html itself; the caller is expected to call
build_site.py once, after all of that scan run's raw-data writes are done
(see build_site.py's own docstring for why merging is centralized there).
"""

import glob
from pathlib import Path

ROOT = Path(__file__).parent


def load_fresh_prices():
    """ticker -> price (float), from fundamentals_data.tsv's Yahoo chart close."""
    prices = {}
    path = ROOT / "fundamentals_data.tsv"
    if not path.exists():
        return prices
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 24:
            continue
        ticker, price = parts[0], parts[5]
        try:
            prices[ticker] = float(price)
        except (ValueError, TypeError):
            continue
    return prices


def main():
    fresh_prices = load_fresh_prices()
    if not fresh_prices:
        print("No fundamentals_data.tsv found or it's empty - run fundamentals_scan.py first.")
        return

    files = sorted(f for f in glob.glob(str(ROOT / "analyst_targets_*.txt")) if "_OLD" not in f)
    total_updated = 0

    for fname in files:
        lines = Path(fname).read_text(encoding="utf-8").split("\n")
        changed = False
        for i, line in enumerate(lines):
            parts = line.split("\t")
            if len(parts) != 8:
                continue
            ticker = parts[0]
            new_price = fresh_prices.get(ticker)
            if new_price is None:
                continue
            parts[2] = f"{new_price:.2f}"
            lines[i] = "\t".join(parts)
            changed = True
            total_updated += 1
        if changed:
            Path(fname).write_text("\n".join(lines), encoding="utf-8")

    print(f"Updated price in {total_updated} rows across {len(files)} files.")


if __name__ == "__main__":
    main()
