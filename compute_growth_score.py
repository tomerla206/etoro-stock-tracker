"""
COMPUTE GROWTH SCORE - a FOURTH, separate 0-10 score, kept apart from the
other three because it answers a different question than any of them: not
"is this stock good" (Score/Secondary Score) or "how volatile is it" (Risk
Score), but "how fast is this company's earnings expected to grow" - across
three different time horizons, all Yahoo consensus estimates:

  1. Earnings Growth (last quarter, YoY) - the most recent REPORTED quarter's
     earnings growth vs. the same quarter a year ago - the only one of the
     three that's a fact, not a forecast, from fundamentals_data.tsv/Yahoo's
     defaultKeyStatistics
  2. EPS Growth Estimate, next year - consensus analyst estimate for EPS
     growth over the next fiscal year, from fundamentals_data.tsv/Yahoo's
     earningsTrend
  3. EPS Growth Estimate, next 5 years - the longest-horizon consensus
     estimate Yahoo publishes (annualized), from fundamentals_data.tsv/
     Yahoo's earningsTrend

Why a fourth score instead of folding these into Score or Secondary Score:
this project already has two "quality" scores and one "volatility" score:
adding growth signals into either would blur what that score means (a high
Score could then mean "cheap and proven" OR "fast-growing but unproven" -
two very different investment cases collapsed into one number). A separate
Growth Score keeps that distinction visible instead of averaging it away -
same reasoning as why Risk Score itself was kept separate from day one.

Same design as the other three: each signal 0-2 points (missing data gets a
neutral 1.0), summed to 0-6 raw, scaled to 0-10 (raw * 10/6), with an X/3
confidence count. NOT blended into Overall Score, same as Risk Score - it's
a different axis, not an independent vote on "quality".

Run: python compute_growth_score.py (after fundamentals_scan.py has produced
fundamentals_data.tsv)
Result: growth_score.tsv (TICKER, score, quarterly_pts, nextyear_pts,
fiveyear_pts, confidence). A raw data file only - does NOT merge into
all_rows.html itself; the caller should call build_site.py once after all of
a scan run's raw-data writes are done (see build_site.py's docstring for why
merging is centralized there).
"""

from pathlib import Path

ROOT = Path(__file__).parent


def load_fundamentals():
    data = {}
    path = ROOT / "fundamentals_data.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 45:
            continue

        def f(v):
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        data[parts[0]] = {
            "earnings_quarterly_growth": f(parts[42]),
            "eps_growth_next_year": f(parts[43]),
            "eps_growth_5y": f(parts[35]),
        }
    return data


def score_growth_pct(growth):
    """Shared shape for all three signals here - each is a Yahoo fraction
    (0.15 = 15%) at a different time horizon, but "fast/slow growth" reads
    the same way regardless of which horizon it's measuring."""
    if growth is None:
        return None
    pct = growth * 100
    if pct > 20:
        return 2.0
    if pct > 10:
        return 1.5
    if pct > 0:
        return 1.0
    if pct > -10:
        return 0.5
    return 0.0


def main():
    fundamentals = load_fundamentals()

    rows = []
    for ticker, fnd in fundamentals.items():
        quarterly_pts_raw = score_growth_pct(fnd.get("earnings_quarterly_growth"))
        nextyear_pts_raw = score_growth_pct(fnd.get("eps_growth_next_year"))
        fiveyear_pts_raw = score_growth_pct(fnd.get("eps_growth_5y"))

        confidence = sum(
            x is not None for x in (quarterly_pts_raw, nextyear_pts_raw, fiveyear_pts_raw)
        )
        if confidence == 0:
            continue

        quarterly_pts = quarterly_pts_raw if quarterly_pts_raw is not None else 1.0
        nextyear_pts = nextyear_pts_raw if nextyear_pts_raw is not None else 1.0
        fiveyear_pts = fiveyear_pts_raw if fiveyear_pts_raw is not None else 1.0

        raw_total = quarterly_pts + nextyear_pts + fiveyear_pts
        total = raw_total * 10 / 6

        rows.append((ticker, total, quarterly_pts, nextyear_pts, fiveyear_pts, confidence))

    with open(ROOT / "growth_score.tsv", "w", encoding="utf-8") as f:
        for ticker, total, quarterly_pts, nextyear_pts, fiveyear_pts, confidence in rows:
            f.write(
                f"{ticker}\t{total:.1f}\t{quarterly_pts:.1f}\t{nextyear_pts:.1f}\t"
                f"{fiveyear_pts:.1f}\t{confidence}\n"
            )

    print(f"Computed Growth Score for {len(rows)} tickers -> growth_score.tsv")


if __name__ == "__main__":
    main()
