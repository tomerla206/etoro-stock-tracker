"""
VERIFY WEEKLY MOMENTUM - end-to-end health check for the whole Weekly
Momentum Score pipeline (momentum_scan.py -> analyst_snapshot.py ->
compute_weekly_momentum.py -> build_weekly_momentum_page.py -> the nav
button in part1_fixed.html). Run this any time after re-running the
pipeline, or periodically, to confirm nothing silently broke.

Prints a PASS/FAIL line per check and exits with code 1 if anything failed
(so it can be wired into a scheduled task or CI-style check later without
needing to parse its stdout by hand).

Run: python verify_weekly_momentum.py
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
STALE_HOURS = 30  # a daily-cadence pipeline shouldn't be older than ~1.25 days

failures = []
warnings_ = []


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" - {detail}" if detail else ""))
    if not condition:
        failures.append(label)


def warn(label, detail=""):
    print(f"[WARN] {label}" + (f" - {detail}" if detail else ""))
    warnings_.append(label)


def file_age_hours(path):
    if not path.exists():
        return None
    return (time.time() - path.stat().st_mtime) / 3600


def count_lines(path, expected_fields=None):
    if not path.exists():
        return 0
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        if expected_fields is not None and len(line.split("\t")) != expected_fields:
            continue
        n += 1
    return n


def main():
    print("=== Weekly Momentum Score - health check ===\n")

    # --- Stage 1: momentum_data.tsv ---
    momentum_file = ROOT / "momentum_data.tsv"
    check("momentum_data.tsv exists", momentum_file.exists())
    if momentum_file.exists():
        n_rows = count_lines(momentum_file, expected_fields=12)
        check("momentum_data.tsv has a sane row count", n_rows >= 500, f"{n_rows} rows")
        age = file_age_hours(momentum_file)
        if age is not None and age > STALE_HOURS:
            warn("momentum_data.tsv looks stale", f"{age:.1f}h old (expected daily refresh)")

    # --- Stage 2: analyst_snapshot_history.tsv ---
    snapshot_file = ROOT / "analyst_snapshot_history.tsv"
    check("analyst_snapshot_history.tsv exists", snapshot_file.exists())
    if snapshot_file.exists():
        n_snap = count_lines(snapshot_file, expected_fields=4)
        check("analyst_snapshot_history.tsv has data", n_snap > 0, f"{n_snap} rows")
        dates = set()
        for line in snapshot_file.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) == 4:
                dates.add(parts[0])
        if len(dates) < 10:
            warn(
                "analyst_snapshot_history.tsv doesn't have enough distinct days yet for the "
                "analyst-revision signal to activate",
                f"{len(dates)} distinct day(s) so far, needs ~14+ (run this daily)",
            )

    # --- Stage 3: weekly_momentum_score.tsv ---
    score_file = ROOT / "weekly_momentum_score.tsv"
    check("weekly_momentum_score.tsv exists", score_file.exists())
    score_rows = 0
    if score_file.exists():
        lines = [l for l in score_file.read_text(encoding="utf-8").splitlines() if l.strip()]
        score_rows = len(lines)
        check("weekly_momentum_score.tsv has a sane row count", score_rows >= 200, f"{score_rows} rows")

        # Rank column should be a clean 1..N sequence with no gaps/dupes.
        ranks = []
        scores_seen = []
        bad_rows = 0
        for line in lines:
            parts = line.split("\t")
            if len(parts) != 10:
                bad_rows += 1
                continue
            try:
                ranks.append(int(parts[0]))
                scores_seen.append(float(parts[2]))
            except ValueError:
                bad_rows += 1
        check("weekly_momentum_score.tsv rows are well-formed (10 fields)", bad_rows == 0, f"{bad_rows} malformed row(s)")
        check("weekly_momentum_score.tsv rank sequence is 1..N with no gaps", ranks == list(range(1, len(ranks) + 1)))
        check(
            "weekly_momentum_score.tsv scores are sorted descending",
            scores_seen == sorted(scores_seen, reverse=True),
        )
        age = file_age_hours(score_file)
        if age is not None and age > STALE_HOURS:
            warn("weekly_momentum_score.tsv looks stale", f"{age:.1f}h old")

    # --- Stage 4: weekly_momentum.html ---
    page_file = ROOT / "weekly_momentum.html"
    check("weekly_momentum.html exists", page_file.exists())
    if page_file.exists() and score_file.exists():
        html = page_file.read_text(encoding="utf-8")
        html_row_count = html.count('class="stock-link"')
        check(
            "weekly_momentum.html's rendered row count matches weekly_momentum_score.tsv",
            html_row_count == score_rows,
            f"page has {html_row_count} linked tickers, data file has {score_rows} rows",
        )
        check("weekly_momentum.html has no leftover template placeholders", "<!--ROWS-->" not in html and "<!--META-->" not in html)
        check("weekly_momentum.html has the disclaimer banner", "אזהרה" in html)

    # --- Stage 5: nav button on the main page ---
    main_page = ROOT / "part1_fixed.html"
    check("part1_fixed.html exists", main_page.exists())
    if main_page.exists():
        html = main_page.read_text(encoding="utf-8")
        check(
            "Nav button linking to weekly_momentum.html exists in part1_fixed.html",
            'href="weekly_momentum.html"' in html,
        )
        # Also check it actually made it into the built site, if that's been rebuilt.
        built_site = ROOT / "nasdaq-stocks.html"
        if built_site.exists():
            built_html = built_site.read_text(encoding="utf-8")
            check(
                "Nav button also present in the rebuilt nasdaq-stocks.html",
                'href="weekly_momentum.html"' in built_html,
            )

    # --- Stage 6: backtest report (informational, not a hard failure if missing) ---
    backtest_file = ROOT / "WEEKLY_MOMENTUM_BACKTEST.md"
    if not backtest_file.exists():
        warn("No backtest report yet", "run backtest_weekly_momentum.py before trusting this with real money")
    else:
        text = backtest_file.read_text(encoding="utf-8")
        if "Edge over random: -" in text or "NO edge over random" in text:
            warn("Latest backtest shows no edge over random selection", "do not trade this live yet")

    print(f"\n=== {len(failures)} failure(s), {len(warnings_)} warning(s) ===")
    if failures:
        print("FAILED CHECKS:")
        for f_ in failures:
            print(f"  - {f_}")
        sys.exit(1)
    print("All hard checks passed.")


if __name__ == "__main__":
    main()
