"""
COMPUTE SCORE CHANGE - flags tickers whose Overall Score moved meaningfully
between the two most recent distinct days in score_history.tsv. A day-to-day
wobble of a few tenths is normal noise (the same signal can flip a 0.5-point
bucket on borderline data); THRESHOLD is set high enough to surface only
moves worth a second look, not every twitch.

Needs at least 2 distinct dates of history for a ticker to say anything -
until then (this project's very first days) this script runs but produces an
empty result, which is expected, not a bug: there is nothing to compare yet.

Run: python compute_score_change.py (after score_history.py has appended
today's row)
Result: score_change.tsv (TICKER, delta, direction, prev_date, latest_date) -
only rows where |delta| >= THRESHOLD; tickers with a small or no change are
simply absent, not written with a zero. A raw data file only - does NOT merge
into all_rows.html itself; the caller should call build_site.py once after all
of a scan run's raw-data writes are done (see build_site.py's docstring for
why merging is centralized there).
"""

from pathlib import Path

ROOT = Path(__file__).parent
HISTORY_FILE = ROOT / "score_history.tsv"
THRESHOLD = 1.0  # Overall Score is 0-10; a swing of 1.0+ point is the bar for "meaningful"


def main():
    if not HISTORY_FILE.exists():
        print("No score_history.tsv found - nothing to compare.")
        return

    # ticker -> {date: overallscore}
    by_ticker = {}
    header_len = None
    for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if header_len is None:
            header_len = len(parts)
        if len(parts) != header_len:
            continue
        date, ticker = parts[0], parts[1]
        overallscore = parts[-2]  # HISTORY_COLUMNS ends [..., "overallscore", "overallscore_confidence"]
        try:
            value = float(overallscore)
        except ValueError:
            continue
        by_ticker.setdefault(ticker, {})[date] = value

    rows = []
    for ticker, dated_values in by_ticker.items():
        dates = sorted(dated_values)
        if len(dates) < 2:
            continue
        prev_date, latest_date = dates[-2], dates[-1]
        delta = dated_values[latest_date] - dated_values[prev_date]
        if abs(delta) >= THRESHOLD:
            direction = "up" if delta > 0 else "down"
            rows.append((ticker, delta, direction, prev_date, latest_date))

    with open(ROOT / "score_change.tsv", "w", encoding="utf-8") as f:
        for ticker, delta, direction, prev_date, latest_date in rows:
            f.write(f"{ticker}\t{delta:.1f}\t{direction}\t{prev_date}\t{latest_date}\n")

    print(f"Computed Score Change for {len(rows)} tickers with a >= {THRESHOLD} point move "
          f"(out of {len(by_ticker)} tickers with any history) -> score_change.tsv")


if __name__ == "__main__":
    main()
