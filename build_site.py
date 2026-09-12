"""
BUILD SITE - the single place that touches all_rows.html and reassembles
nasdaq-stocks.html. Runs every merge_*.py script in sequence (never
concurrently) and then writes nasdaq-stocks.html.

Why this exists (2026-09-06): individual scan scripts used to each call their
own merge script and reassemble the site at their own end. When multiple
scans run concurrently (the whole point of the "Run All Background" button -
parallel scanning is what saves time), this caused a classic lost-update
race: two scripts independently read-modify-wrote the same all_rows.html, and
whichever finished last silently wiped out whatever the other had just
merged in (this is exactly how AAPL's Yahoo dividend data vanished from the
site despite being correctly scraped and sitting in yahoo_dividends_*.txt the
whole time).

The fix keeps every scan script's actual DATA COLLECTION fully parallel
(each writes only its own independent file - analyst_targets_*.txt,
insider_activity.tsv, fundamentals_data.tsv, yahoo_dividends_*.txt, etc. -
no two scans ever share an output file, so there's nothing to race on there).
Only the RENDER step - turning all those independent files into one
all_rows.html - is now serialized into this single script, called once by
whichever scan finishes and wants the site rebuilt. Running the merges
sequentially in one process means each step fully finishes and saves before
the next one starts reading, so there is no window where two steps can
clobber each other - and since each merge script only ever touches its own
slice of each <tr>'s attributes (data-cons/data-rating for consensus,
data-ins-* for insider, data-yh-div for dividends, etc.), running them
one-after-another can only ever ADD data, never erase a sibling script's work.

A simple file lock covers the residual case of two scan processes finishing
around the same moment and both trying to call this script at once - the
second one just waits for the first's rebuild to finish rather than running
concurrently against it.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
LOCK_FILE = ROOT / ".build_site.lock"
LOCK_STALE_SECONDS = 120  # a lock older than this is assumed to be from a crashed run, not a real one

MERGE_SCRIPTS = [
    "merge_analyst_targets.py",
    "merge_elevated_risk.py",
    "merge_yahoo_targets.py",
    "merge_yahoo_dividends.py",
    "merge_consensus.py",
    "merge_hedgefund.py",
    "merge_insider.py",
    "merge_fundamentals.py",
    "merge_score.py",
    "merge_secondary_score.py",
    "merge_risk_score.py",
    "merge_growth_score.py",
    "merge_overall_score.py",
    "merge_score_percentile.py",
    "merge_portfolio.py",
    "merge_scan_dates.py",
    # Must run LAST: tags each row with data-currency/data-target-currency for
    # the UI's $/GBX/etc. labels. It isn't wired into any of the scripts above
    # (it only ever ran when someone remembered to launch it by hand), so its
    # labels were silently wiped by the very next automated rebuild - found
    # 2026-09-10 while fixing a stale TARGET_CURRENCY_OVERRIDE entry, since a
    # dormant feature is much easier to leave stale than one that runs daily.
    "add_currency_labels.py",
]


def acquire_lock():
    while True:
        try:
            fd = open(LOCK_FILE, "x", encoding="utf-8")
            fd.write(str(time.time()))
            fd.close()
            return
        except FileExistsError:
            try:
                age = time.time() - LOCK_FILE.stat().st_mtime
            except FileNotFoundError:
                continue  # lock was released between our open() failing and this stat()
            if age > LOCK_STALE_SECONDS:
                try:
                    LOCK_FILE.unlink()
                except FileNotFoundError:
                    pass
                continue
            time.sleep(0.5)


def release_lock():
    try:
        LOCK_FILE.unlink()
    except FileNotFoundError:
        pass


def main():
    acquire_lock()
    failed = []
    try:
        for script in MERGE_SCRIPTS:
            if not (ROOT / script).exists():
                continue
            result = subprocess.run(
                [sys.executable, script], cwd=ROOT, capture_output=True, text=True
            )
            output = (result.stdout or "").strip()
            if output:
                print(f"[{script}] {output}")
            if result.returncode != 0:
                print(f"WARNING: {script} exited with code {result.returncode}:\n{result.stderr}")
                failed.append(script)

        # Write to a temp file and rename into place rather than writing
        # nasdaq-stocks.html directly, so a crash/kill mid-write (Task
        # Manager kill, power loss) can never leave a truncated site file -
        # os.replace is atomic on both Windows and POSIX.
        tmp_path = ROOT / "nasdaq-stocks.html.tmp"
        with open(tmp_path, "w", encoding="utf-8") as out:
            for part in ("part1_fixed.html", "all_rows.html", "part3.html"):
                out.write((ROOT / part).read_text(encoding="utf-8"))
        os.replace(tmp_path, ROOT / "nasdaq-stocks.html")

        if failed:
            print(f"Site rebuilt WITH {len(failed)} merge failure(s): {', '.join(failed)}")
        else:
            print("Site rebuilt: nasdaq-stocks.html")
    finally:
        release_lock()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
