"""
BACKTEST SIGNALS - checks whether any of the ~26 scoring signals in
score_history.tsv actually correlate with FUTURE price moves, instead of
just assuming they do because the reasoning behind each one sounds
plausible. Built in response to a direct question: "can this system
reliably tell me what to buy/sell today for same-day profit?" - the honest
answer is "not from daily EOD data, and not without checking" - this is
the checking part.

No external price data needed: score_history.tsv already stores a daily
price snapshot per ticker alongside every score component, so a forward
return is just comparing the SAME ticker's price on two of its own rows.

Methodology:
  1. For each ticker, sorted by date, take every pair of snapshots that are
     H snapshots apart (H = 1/5/20, roughly next-day/next-week/next-month
     given scans run about once a day) and compute the forward return:
     (price_later - price_now) / price_now * 100.
  2. Market-relative alpha: subtract that START date's AVERAGE forward
     return across every ticker with a valid pair at that horizon. This
     matters a lot - on a day the whole market rallies 3%, every bucket
     would look "profitable" even for a signal with zero real predictive
     power. Alpha isolates whatever the signal itself is contributing,
     not general market drift.
  3. Bucket tickers by their signal value on the EARLIER date (the day the
     "prediction" would have been made) and report the average alpha per
     bucket. Each _pts component naturally lands on one of 5 values
     (0/0.5/1/1.5/2 - however that signal's own scoring function was
     written), so those buckets exist for free; the five continuous score
     totals (0-10) are grouped into 2-point-wide ranges instead, or the
     table would be one row per unique decimal value.

Reading the result: if a signal has real predictive power, its bucket
table should show average alpha climbing (or falling) monotonically
alongside the signal value, holding up across more than one horizon and
with a reasonable sample size per bucket (n) - a pattern in a bucket with
n=4 is noise, not a finding. A signal that shows no relationship, or an
inconsistent one that flips sign between horizons, is not carrying real
short-term predictive information - that's a legitimate finding too, not
a failure of this script.

Needs enough distinct daily snapshots to form pairs at the longest horizon
tested (20) - with score_history.tsv freshly started, this will report
"not enough history yet" and do nothing else until enough daily scans
(local or cloud) have accumulated. Re-run anytime; it only reads
score_history.tsv and never writes to it or any other score/site file.

Run: python backtest_signals.py
Result: BACKTEST_RESULTS.md
"""

from collections import defaultdict
from pathlib import Path

import score_history as sh

ROOT = Path(__file__).parent
HISTORY_FILE = ROOT / "score_history.tsv"
RESULTS_FILE = ROOT / "BACKTEST_RESULTS.md"

HORIZONS = [1, 5, 20]  # snapshots ahead, not calendar days

# Every per-component point column plus each score's own total - pulled
# directly from score_history.py's own column list so this never drifts
# out of sync with what that script actually writes.
PTS_COLUMNS = [c for c in sh.HISTORY_COLUMNS if c.endswith("_pts")]
TOTAL_COLUMNS = ["score", "secscore", "riskscore", "growthscore", "overallscore"]


def f(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def load_history():
    """ticker -> list of row dicts, sorted by date, each with a validated
    numeric _price attached."""
    by_ticker = defaultdict(list)
    if not HISTORY_FILE.exists():
        return by_ticker
    with open(HISTORY_FILE, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != len(sh.HISTORY_COLUMNS):
                continue
            row = dict(zip(sh.HISTORY_COLUMNS, parts))
            price = f(row.get("price"))
            if not price or price <= 0:
                continue
            row["_price"] = price
            by_ticker[row["ticker"]].append(row)
    for ticker in by_ticker:
        by_ticker[ticker].sort(key=lambda r: r["date"])
    return by_ticker


def bucket_key(col, value):
    """Returns (sort_key, label) for grouping. _pts columns already only
    take 5 discrete values (however that signal's own scorer wrote them),
    so the raw value IS the bucket. Continuous 0-10 totals get grouped into
    2-point-wide ranges instead, or every unique decimal would get its own
    near-empty row."""
    if col in TOTAL_COLUMNS:
        lo = int(value // 2) * 2
        return (lo, f"{lo}-{lo + 2}")
    return (value, str(value))


def main():
    by_ticker = load_history()
    distinct_dates = sorted({row["date"] for rows in by_ticker.values() for row in rows})
    print(f"Loaded {len(by_ticker)} tickers across {len(distinct_dates)} distinct day(s) of history.")

    max_horizon = max(HORIZONS)
    if len(distinct_dates) <= max_horizon:
        msg = (
            f"Not enough history yet to backtest - the longest horizon tested ({max_horizon} "
            f"snapshots) needs at least {max_horizon + 1} distinct days, only {len(distinct_dates)} "
            f"exist so far. This accumulates automatically every time FUNDAMENTALS SCAN runs "
            f"(locally or in the daily cloud workflow) - just re-run `python backtest_signals.py` "
            f"again in a few weeks, no other action needed."
        )
        print(msg)
        with open(RESULTS_FILE, "w", encoding="utf-8") as out:
            out.write("# Backtest Results\n\n" + msg + "\n")
        return

    # Build (ticker, start_row, forward_return_pct) triples per horizon.
    per_horizon = {h: [] for h in HORIZONS}
    for ticker, rows in by_ticker.items():
        n = len(rows)
        for h in HORIZONS:
            for i in range(n - h):
                today, future = rows[i], rows[i + h]
                ret = (future["_price"] - today["_price"]) / today["_price"] * 100
                per_horizon[h].append((ticker, today, ret))

    # Market-relative alpha: subtract the average forward return of every
    # ticker that started on the SAME date at the SAME horizon, so a
    # generally rising/falling market that day doesn't get credited to
    # whatever signal happens to be high/low that day.
    for h in HORIZONS:
        by_start_date = defaultdict(list)
        for ticker, today, ret in per_horizon[h]:
            by_start_date[today["date"]].append(ret)
        market_avg = {d: sum(rs) / len(rs) for d, rs in by_start_date.items()}
        per_horizon[h] = [
            (ticker, today, ret - market_avg[today["date"]])
            for ticker, today, ret in per_horizon[h]
        ]

    lines = [
        "# Backtest Results\n\n",
        f"Based on {len(distinct_dates)} distinct day(s) of history across {len(by_ticker)} tickers.\n\n",
        "**Alpha** = forward return minus that start-date's average forward return across all "
        "tickers at the same horizon (removes overall market movement for that day, isolating "
        "whatever the signal itself contributed). Read the per-signal tables below for whether "
        "alpha climbs (or falls) consistently as the signal's value increases, across more than "
        "one horizon, with a real sample size (`n`) per bucket - anything else is noise, not a "
        "finding.\n\n",
    ]

    for h in HORIZONS:
        records = per_horizon[h]
        lines.append(f"## Horizon: {h} snapshot(s) ahead ({len(records)} ticker-day pairs)\n\n")
        if not records:
            lines.append("No pairs available at this horizon yet.\n\n")
            continue
        for col in PTS_COLUMNS + TOTAL_COLUMNS:
            buckets = defaultdict(list)
            for ticker, today, alpha in records:
                v = f(today.get(col))
                if v is None:
                    continue
                buckets[bucket_key(col, v)].append(alpha)
            if not buckets:
                continue
            lines.append(f"**{col}**\n\n| value | n | avg alpha % |\n|---|---|---|\n")
            for key in sorted(buckets):
                alphas = buckets[key]
                avg = sum(alphas) / len(alphas)
                lines.append(f"| {key[1]} | {len(alphas)} | {avg:+.2f} |\n")
            lines.append("\n")

    with open(RESULTS_FILE, "w", encoding="utf-8") as out:
        out.writelines(lines)

    print(f"Backtest complete -> {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
