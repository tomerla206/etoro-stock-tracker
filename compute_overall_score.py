"""
COMPUTE OVERALL SCORE - a single blended 0-10 number combining Score (weight
0.7) and Secondary Score (weight 0.3), for anyone who wants one number instead
of comparing two. Deliberately does NOT include Risk Score - Risk Score
measures volatility/instability, not quality, and blending a "how wild is
this stock" axis into a "how good is this stock" number would make the result
meaningless (a highly volatile stock isn't better OR worse than a calm one on
its own - see Risk Score's own tooltip). Weighted 0.7/0.3 rather than a plain
average because Score's 8 signals include harder facts (Rating, Insider $,
Short Interest) while Secondary Score's 6 signals are explicitly the weaker,
more uncertain ones (PEG, Hedge Fund sample, Volume Spike, EPS Trend, Margin,
Growth) - see each score's own docstring for why they were kept separate to
begin with. If a ticker only has one of the two, that one is used alone
(weight redistributed to 1.0) rather than treating the missing one as a 0.

Run: python compute_overall_score.py (after both compute_score.py and
compute_secondary_score.py have produced score.tsv/secondary_score.tsv)
Result: overall_score.tsv (TICKER, overall, score_component, secscore_component,
confidence). confidence is the SUM of both scores' own confidence counts
(max 15+18=33), not a new independent measurement - it's inherited, not
recomputed. A raw data file only - does NOT merge into all_rows.html itself;
the caller should call build_site.py once after all of a scan run's raw-data
writes are done (see build_site.py's docstring for why merging is centralized
there).
"""

from pathlib import Path

ROOT = Path(__file__).parent

SCORE_WEIGHT = 0.7
SECSCORE_WEIGHT = 0.3


def load_score():
    data = {}
    path = ROOT / "score.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 18:
            continue
        ticker, total, *_rest, confidence = parts
        try:
            data[ticker] = (float(total), int(confidence))
        except ValueError:
            continue
    return data


def load_secondary_score():
    data = {}
    path = ROOT / "secondary_score.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 21:
            continue
        ticker, total, *_rest, confidence = parts
        try:
            data[ticker] = (float(total), int(confidence))
        except ValueError:
            continue
    return data


def main():
    scores = load_score()
    secondary = load_secondary_score()

    rows = []
    for ticker in set(scores) | set(secondary):
        score_val = scores.get(ticker)
        sec_val = secondary.get(ticker)

        if score_val is not None and sec_val is not None:
            overall = score_val[0] * SCORE_WEIGHT + sec_val[0] * SECSCORE_WEIGHT
        elif score_val is not None:
            overall = score_val[0]
        else:
            overall = sec_val[0]

        confidence = (score_val[1] if score_val else 0) + (sec_val[1] if sec_val else 0)
        rows.append((
            ticker, overall,
            score_val[0] if score_val else None,
            sec_val[0] if sec_val else None,
            confidence,
        ))

    with open(ROOT / "overall_score.tsv", "w", encoding="utf-8") as f:
        for ticker, overall, score_component, secscore_component, confidence in rows:
            f.write(
                f"{ticker}\t{overall:.1f}\t"
                f"{score_component if score_component is not None else ''}\t"
                f"{secscore_component if secscore_component is not None else ''}\t"
                f"{confidence}\n"
            )

    print(f"Computed Overall Score for {len(rows)} tickers -> overall_score.tsv")


if __name__ == "__main__":
    main()
