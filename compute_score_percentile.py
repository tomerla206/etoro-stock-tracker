"""
COMPUTE SCORE PERCENTILE - ranks each ticker's Overall Score against only its
own sector's peers, not the whole universe. A Score of 7 in Technology (a
sector full of high scorers) may be mediocre, while a 7 in Utilities (usually
lower scorers) may be near the top - the raw Overall Score alone can't tell
you that, so this adds a second, relative lens next to the absolute one.

Percentile = the share of same-sector tickers this ticker's Overall Score
beats or ties (0-100, higher = better within-sector standing). Only computed
for sectors with at least MIN_SECTOR_SIZE tickers - with too few peers a
"percentile" is close to meaningless (one company can swing from 0th to 100th
by itself), so those tickers get no percentile rather than a misleading one.

Run: python compute_score_percentile.py (after compute_overall_score.py and
fundamentals_scan.py's sector_data.tsv both exist)
Result: score_percentile.tsv (TICKER, percentile, sector, sector_size). A raw
data file only - does NOT merge into all_rows.html itself; the caller should
call build_site.py once after all of a scan run's raw-data writes are done
(see build_site.py's docstring for why merging is centralized there).
"""

from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
MIN_SECTOR_SIZE = 5


def load_sectors():
    data = {}
    path = ROOT / "sector_data.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        ticker, sector, _industry = parts
        if sector:
            data[ticker] = sector
    return data


def load_overall_scores():
    data = {}
    path = ROOT / "overall_score.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 5:
            continue
        ticker, total, *_rest = parts
        try:
            data[ticker] = float(total)
        except ValueError:
            continue
    return data


def main():
    sectors = load_sectors()
    scores = load_overall_scores()

    by_sector = defaultdict(list)
    for ticker, sector in sectors.items():
        if ticker in scores:
            by_sector[sector].append((ticker, scores[ticker]))

    rows = []
    for sector, members in by_sector.items():
        if len(members) < MIN_SECTOR_SIZE:
            continue
        values = sorted(v for _t, v in members)
        n = len(values)
        for ticker, value in members:
            beaten_or_tied = sum(1 for v in values if v <= value)
            percentile = beaten_or_tied / n * 100
            rows.append((ticker, percentile, sector, n))

    with open(ROOT / "score_percentile.tsv", "w", encoding="utf-8") as f:
        for ticker, percentile, sector, n in rows:
            f.write(f"{ticker}\t{percentile:.0f}\t{sector}\t{n}\n")

    print(f"Computed Score Percentile for {len(rows)} tickers across {len(by_sector)} sectors "
          f"({sum(1 for s in by_sector.values() if len(s) < MIN_SECTOR_SIZE)} sectors skipped, too small) "
          f"-> score_percentile.tsv")


if __name__ == "__main__":
    main()
