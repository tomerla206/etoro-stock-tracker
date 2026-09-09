"""
Incremental updater for exit_history.tsv, replacing the old "re-scrape
everything from scratch" workflow with a checkpoint-based one.

Why this exists: eToro's /portfolio/history page requires a live logged-in
browser session and can't be scraped headlessly, so each update still means
a human (via Claude driving the browser) scrolling the page and transcribing
newly-closed profitable positions into a small batch file - same format as
before: TICKER\texit_date(YYYY-MM-DD)\texit_price\tpl_pct\taccount, one row
per line. What this script adds on top is a persistent checkpoint
(scan_checkpoint.json) recording, per account, the latest exit_date already
covered and when that scan was run - so next time, only the batches with
exit_date AFTER the checkpoint need to be transcribed at all; scrolling can
stop as soon as the page reaches that date instead of going all the way to
the start of the account's history.

Run: python update_exit_history.py <batch_file> <real|virtual>
Effect:
  - Merges <batch_file>'s rows into exit_history.tsv (upsert by
    ticker+exit_date+account, same as parse_exit_history.py).
  - Updates scan_checkpoint.json[<account>] to the max exit_date now present
    for that account, plus today's date as last_scanned_on.
Then, with no arguments, prints the current checkpoint for both accounts -
run it bare before starting a new scan session to see where to resume from.
"""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
EXIT_HISTORY_FILE = ROOT / "exit_history.tsv"
CHECKPOINT_FILE = ROOT / "scan_checkpoint.json"


def load_existing():
    existing = {}
    if EXIT_HISTORY_FILE.exists():
        for line in EXIT_HISTORY_FILE.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) != 5:
                continue
            key = (parts[0], parts[1], parts[4])
            existing[key] = line
    return existing


def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
    return {}


def save_checkpoint(checkpoint):
    CHECKPOINT_FILE.write_text(
        json.dumps(checkpoint, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def max_exit_date(existing, account):
    dates = [k[1] for k in existing if k[2] == account]
    return max(dates) if dates else None


def print_status():
    existing = load_existing()
    checkpoint = load_checkpoint()
    for account in ("real", "virtual"):
        count = sum(1 for k in existing if k[2] == account)
        newest = max_exit_date(existing, account)
        cp = checkpoint.get(account, {})
        print(f"[{account}] {count} records | newest exit_date in file: {newest}")
        if cp:
            print(f"    last checkpoint: {cp.get('last_exit_date')} "
                  f"(scanned on {cp.get('last_scanned_on')})")
        else:
            print("    no checkpoint recorded yet")


def main():
    if len(sys.argv) == 1:
        print_status()
        return

    if len(sys.argv) != 3 or sys.argv[2] not in ("real", "virtual"):
        print("Usage:")
        print("  python update_exit_history.py                       # show checkpoint status")
        print("  python update_exit_history.py <batch_file> <real|virtual>  # merge a new batch")
        sys.exit(1)

    batch_path = Path(sys.argv[1])
    account = sys.argv[2]

    existing = load_existing()
    before_count = len(existing)

    new_rows = 0
    for line in batch_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 5:
            print(f"  skipping malformed line: {line!r}")
            continue
        ticker, exit_date, exit_price, pl_pct, row_account = parts
        if row_account != account:
            print(f"  warning: row account {row_account!r} != {account!r} argument, using {account!r}")
            row_account = account
        key = (ticker, exit_date, row_account)
        if key not in existing:
            new_rows += 1
        existing[key] = f"{ticker}\t{exit_date}\t{exit_price}\t{pl_pct}\t{row_account}"

    with open(EXIT_HISTORY_FILE, "w", encoding="utf-8") as f:
        for key in sorted(existing):
            f.write(existing[key] + "\n")

    checkpoint = load_checkpoint()
    newest = max_exit_date(existing, account)
    checkpoint[account] = {
        "last_exit_date": newest,
        "last_scanned_on": date.today().isoformat(),
    }
    save_checkpoint(checkpoint)

    print(f"Merged {batch_path.name}: {new_rows} new row(s), "
          f"{len(existing) - before_count - new_rows} overwritten dupe(s).")
    print(f"exit_history.tsv now has {len(existing)} total records.")
    print(f"[{account}] checkpoint updated: newest exit_date = {newest}, "
          f"scanned on {checkpoint[account]['last_scanned_on']}")


if __name__ == "__main__":
    main()
