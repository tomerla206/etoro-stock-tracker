"""
ANALYST SNAPSHOT - daily append-only log of each ticker's analyst average
target price, feeding the Weekly Momentum Score's "analyst revision" signal
(see WEEKLY_MOMENTUM_STATE.json). Research basis: a CHANGE in analyst
targets/ratings over the last 1-4 weeks is a much stronger short-term signal
than the static rating level (which the main Score already uses) - see the
Jegadeesh/Kim/Krische analyst-revision-momentum literature cited in the
2026-09-13 research summary.

Idempotent per day, same pattern as score_history.py: re-running today
replaces today's rows instead of duplicating them, so this is safe to call
more than once on the same day (e.g. once from the morning FUNDAMENTALS SCAN
chain, again manually later).

This deliberately does NOT try to backfill history - it only ever appends
"today". compute_analyst_revision() will report None/neutral for every
ticker until ~14-21 days of accumulated snapshots exist (same limitation as
score_history.py's own change-detection, documented there too). That's
expected, not a bug - there is no free source of historical analyst-target
snapshots to backfill from.

Run: python analyst_snapshot.py (after analyst_targets_*.txt is fresh)
Result: analyst_snapshot_history.tsv (append-only, DATE\\tTICKER\\tAVG_TARGET\\tSTATUS)
"""

import glob
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
HISTORY_FILE = ROOT / "analyst_snapshot_history.tsv"


def load_today_targets():
    """ticker -> (avg_target, status), from analyst_targets_*.txt (same
    source/parsing convention as merge_analyst_targets.py)."""
    data = {}
    files = sorted(fn for fn in glob.glob(str(ROOT / "analyst_targets_*.txt")) if "_OLD" not in fn)
    for fname in files:
        for line in Path(fname).read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != 8:
                continue
            ticker, _name, _price, _low, avg, _high, status, _trade = parts
            if status not in ("OK", "CVR"):
                continue
            try:
                avg_f = float(avg)
            except (ValueError, TypeError):
                continue
            data[ticker] = (avg_f, status)
    return data


def main():
    today = date.today().isoformat()
    today_targets = load_today_targets()
    if not today_targets:
        print("No analyst_targets_*.txt data found - nothing to snapshot.")
        return

    existing_lines = []
    if HISTORY_FILE.exists():
        for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) == 4 and parts[0] == today:
                continue  # drop today's old rows, replaced below
            if parts and parts[0]:
                existing_lines.append(line)

    new_lines = [f"{today}\t{ticker}\t{avg}\t{status}" for ticker, (avg, status) in today_targets.items()]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(existing_lines + new_lines) + "\n")

    print(f"Snapshotted {len(new_lines)} tickers for {today} -> {HISTORY_FILE.name} "
          f"({len(existing_lines)} prior rows kept)")


def compute_analyst_revision(min_days_back=14, max_days_back=25):
    """ticker -> revision_pct (change in avg target over the last min_days_back
    to max_days_back window, as a % of the older value), for every ticker that
    has a snapshot both today and somewhere in that window. Returns {} if
    there isn't enough history yet (expected for the first ~2-3 weeks after
    this script starts running daily)."""
    if not HISTORY_FILE.exists():
        return {}

    by_date = {}
    for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 4:
            continue
        snap_date, ticker, avg, _status = parts
        try:
            avg_f = float(avg)
        except (ValueError, TypeError):
            continue
        by_date.setdefault(snap_date, {})[ticker] = avg_f

    dates = sorted(by_date.keys())
    if len(dates) < 2:
        return {}
    today_str = dates[-1]
    today_map = by_date[today_str]

    # Pick the reference date closest to (but not more recent than) today
    # minus min_days_back, within the max_days_back window - a plain
    # calendar-day count, close enough for this purpose since eToro/TipRanks
    # updates aren't tied to trading-day precision anyway.
    today_date = date.fromisoformat(today_str)
    candidates = [
        d for d in dates[:-1]
        if min_days_back <= (today_date - date.fromisoformat(d)).days <= max_days_back
    ]
    if not candidates:
        return {}
    ref_date = max(candidates)  # closest to min_days_back within the window
    ref_map = by_date[ref_date]

    revisions = {}
    for ticker, today_avg in today_map.items():
        ref_avg = ref_map.get(ticker)
        if ref_avg is None or ref_avg == 0:
            continue
        revisions[ticker] = (today_avg - ref_avg) / ref_avg * 100
    return revisions


if __name__ == "__main__":
    main()
