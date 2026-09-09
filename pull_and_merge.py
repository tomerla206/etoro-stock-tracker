"""
PULL AND MERGE - the new local daily-refresh step, replacing local scan runs
now that MEGASCAN/MEGASCAN YAHOO/INSIDER SCAN/FUNDAMENTALS SCAN all run in
the cloud instead (see .github/workflows/daily-scan.yml). This script:

  1. `git pull` - fetches the cloud's freshly-scanned public data (analyst
     targets, fundamentals, all 4 scores, sector percentile, etc.) and its
     regenerated all_rows.html/nasdaq-stocks.html (portfolio-free).
  2. `python build_site.py` - re-runs every merge script locally, including
     merge_portfolio.py, which reads the LOCAL-ONLY portfolio_virtual.tsv/
     portfolio_real.tsv (never pulled, never pushed) and re-injects your real
     holdings into the freshly-pulled site.

Why this is safe from git's perspective: the git "clean filter"
(sanitize_portfolio.py, wired via .gitattributes) strips portfolio data out
of all_rows.html/nasdaq-stocks.html/index.html every time git looks at them
for a diff - so merge_portfolio.py's local edits are invisible to git and
never conflict with a future `git pull`. This only holds as long as nothing
else modifies the PUBLIC parts of these files locally (i.e. don't run
megascan.py/fundamentals_scan.py/etc. locally anymore - that's the cloud's
job now); if you ever need to force a fresh local scan anyway, that's still
fine to do by hand, just expect this script's next `git pull` to need a
manual conflict resolution once.

Run: python pull_and_merge.py (this is what the two local Scheduled Tasks -
"eToro FUNDAMENTALS SCAN" and "eToro Daily Scan (MEGASCAN + MEGASCAN YAHOO)"
- now run instead of the actual scan scripts, since the cloud is that data's
source of truth). Also runnable on demand via the site's "Pull Updates"
button (POST /run/pull on portfolio_server.py) - see index.html/part1_fixed.html's
scan-status-row for it, and PULL_LOG.md below for how its "last: Xh ago"
status is tracked the same way as every other scan button.

Writes PULL_LOG.md when done (a single summary line + timestamp) purely so
portfolio_server.py's existing /status polling (built for the scan scripts'
own *_LOG.md files) can show this one's "last pulled" time in the site's
scan-status row for free, without any server-side special-casing.
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
LOG_FILE = ROOT / "PULL_LOG.md"


def write_log(message):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    LOG_FILE.write_text(f"{message}\nLast attempt: {timestamp}\n", encoding="utf-8")


def main():
    print("Pulling latest scan results from GitHub...")
    result = subprocess.run(["git", "pull", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"WARNING: git pull failed:\n{result.stderr}")
        print("Skipping local merge - site keeps whatever data it already had.")
        write_log(f"Pull failed (site keeps existing data): {result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'unknown error'}")
        return

    already_up_to_date = "Already up to date" in result.stdout
    print("Merging local portfolio data into the freshly-pulled site...")
    subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=False)
    write_log("Already up to date" if already_up_to_date else "Pulled new data and rebuilt site")


if __name__ == "__main__":
    main()
