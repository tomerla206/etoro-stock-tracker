"""
One-time/manual helper: parses a raw text dump copied from eToro's own
https://www.etoro.com/portfolio/history page (filtered to "Manual Trades",
extracted via get_page_text - see REFRESH_METHOD.md's SCAN EXIT HISTORY
section for the exact live-session steps, since eToro's history page
requires a real logged-in session and can't be scraped headlessly) into
exit_history.tsv - a permanent log of realized-profit exits used by
check_reentry_opportunities.py to watch for a good re-entry point later.

Input format (one raw text block per closed position, as it comes out of
get_page_text on that page): "BUY TICKER", optionally "CFD" on its own
line, then Invested/Units/Open price/Open date/Open time/Close price/
Close date/Close time/P&L($)/P&L(%), each on its own line.

Only keeps rows that are BOTH actually closed (has a Close date) AND
closed at a profit (P/L% > 0) - a stop-loss exit or a still-open position
isn't what this log is for; re-entry logic only makes sense for a
position you deliberately sold to lock in a gain.

Run: python parse_exit_history.py <raw_text_file> <account: real|virtual>
Result: appends to exit_history.tsv (TICKER, exit_date, exit_price,
pl_pct, account) - does not overwrite existing rows for other
tickers/accounts, so this can be re-run for each account/each new batch
of history without losing earlier entries. Re-running for the SAME
ticker+exit_date+account replaces that one row (idempotent).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
EXIT_HISTORY_FILE = ROOT / "exit_history.tsv"


def parse_date(d):
    """DD/MM/YYYY -> YYYY-MM-DD"""
    day, month, year = d.split("/")
    return f"{year}-{month}-{day}"


def parse_blocks(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    records = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith("BUY "):
            i += 1
            continue
        ticker = lines[i][len("BUY "):].strip()
        i += 1
        if i < len(lines) and lines[i] == "CFD":
            i += 1
        # Expect: invested, units, open_price, open_date, open_time,
        # close_price, close_date, close_time, pl_dollar, pl_pct
        try:
            invested = lines[i]; i += 1
            units = lines[i]; i += 1
            open_price = lines[i]; i += 1
            open_date = lines[i]; i += 1
            open_time = lines[i]; i += 1
            close_price = lines[i]; i += 1
            close_date = lines[i]; i += 1
            close_time = lines[i]; i += 1
            pl_dollar = lines[i]; i += 1
            pl_pct = lines[i]; i += 1
        except IndexError:
            break

        # A still-open position has no close date (its line at that
        # position would be the START of the next "BUY ..." block, or
        # something not matching DD/MM/YYYY) - skip rather than
        # misparse it as a closed one.
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", close_date):
            # Rewind - this "record" was actually shorter (still open);
            # re-process the lines we over-consumed as fresh input.
            i -= 10
            i += 1
            continue

        records.append({
            "ticker": ticker,
            "close_price": close_price,
            "close_date": close_date,
            "pl_pct": pl_pct,
        })
    return records


def fnum(v):
    try:
        return float(v.replace("$", "").replace(",", "").replace("%", ""))
    except (ValueError, AttributeError):
        return None


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("real", "virtual"):
        print("Usage: python parse_exit_history.py <raw_text_file> <real|virtual>")
        sys.exit(1)

    raw_path = Path(sys.argv[1])
    account = sys.argv[2]
    text = raw_path.read_text(encoding="utf-8")
    records = parse_blocks(text)

    profitable = []
    for r in records:
        pl_pct = fnum(r["pl_pct"])
        exit_price = fnum(r["close_price"])
        if pl_pct is None or exit_price is None or pl_pct <= 0:
            continue
        profitable.append({
            "ticker": r["ticker"],
            "exit_date": parse_date(r["close_date"]),
            "exit_price": exit_price,
            "pl_pct": pl_pct,
            "account": account,
        })

    print(f"Parsed {len(records)} closed positions, {len(profitable)} were profitable exits.")

    # Load existing log, replace matching (ticker, exit_date, account) rows.
    existing = {}
    if EXIT_HISTORY_FILE.exists():
        for line in EXIT_HISTORY_FILE.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) != 5:
                continue
            key = (parts[0], parts[1], parts[4])
            existing[key] = line

    for row in profitable:
        key = (row["ticker"], row["exit_date"], row["account"])
        existing[key] = (
            f"{row['ticker']}\t{row['exit_date']}\t{row['exit_price']}\t"
            f"{row['pl_pct']}\t{row['account']}"
        )

    with open(EXIT_HISTORY_FILE, "w", encoding="utf-8") as f:
        for key in sorted(existing):
            f.write(existing[key] + "\n")

    print(f"exit_history.tsv now has {len(existing)} total exit records.")


if __name__ == "__main__":
    main()
