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
never conflict with a future `git pull`.

scan_values.py (SCAN VALUES, auto-chained by SCAN HOLDINGS) is the one
exception to "nothing else modifies the PUBLIC parts of these files
locally": it writes held-ticker refreshes directly into the same shared,
cloud-updated files (analyst_targets_*.txt, consensus_ratings.txt,
insider_activity.tsv), which - unlike the git-clean-filtered files above -
git sees as genuinely dirty. Found 2026-09-12: this silently blocked every
`git pull` (and therefore every auto-pull-on-page-load) for TWO DAYS
straight, since the failure only ever showed up as an unchanged "Pull
Updates" timestamp with no visible error on the site itself. Rather than
ban running SCAN VALUES locally (it's the whole point of SCAN HOLDINGS
auto-chaining it), this script now recovers automatically: on a pull
failure caused by local changes, it discards local changes to exactly the
files git names as blocking the merge (they're always about to be
overwritten by the cloud's fresher full-universe scan anyway - nothing of
value is lost) and retries the pull once.

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

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
LOG_FILE = ROOT / "PULL_LOG.md"

# Matches git's "error: Your local changes to the following files would be
# overwritten by merge:\n\tfile1\n\tfile2\n..." block, ending at the next
# line that isn't a tab-indented file path.
OVERWRITE_ERROR_RE = re.compile(
    r"Your local changes to the following files would be overwritten by merge:\n((?:\t.+\n?)+)"
)


def write_log(message):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    LOG_FILE.write_text(f"{message}\nLast attempt: {timestamp}\n", encoding="utf-8")


def git_pull():
    return subprocess.run(["git", "pull", "origin", "main"], cwd=ROOT, capture_output=True, text=True)


def discard_blocking_files(stderr):
    """If git's failure lists specific files as blocking the merge, discard
    local changes to exactly those (and only those) files. Returns the list
    discarded, or an empty list if the error didn't match that shape."""
    match = OVERWRITE_ERROR_RE.search(stderr)
    if not match:
        return []
    files = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    if not files:
        return []
    subprocess.run(["git", "checkout", "--"] + files, cwd=ROOT, check=False)
    return files


def main():
    print("Pulling latest scan results from GitHub...")
    result = git_pull()
    print(result.stdout)

    if result.returncode != 0:
        discarded = discard_blocking_files(result.stderr)
        if discarded:
            # scan_values.py (run locally by SCAN HOLDINGS) writes held-
            # ticker refreshes straight into these same cloud-updated
            # files - always safe to drop in favor of the cloud's fresher
            # full-universe scan and retry, see module docstring.
            print(f"Local changes to {len(discarded)} file(s) were blocking the pull "
                  f"(likely from a local SCAN VALUES run) - discarded and retrying:")
            print("  " + "\n  ".join(discarded))
            result = git_pull()
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
