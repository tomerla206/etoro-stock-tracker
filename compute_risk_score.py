"""
COMPUTE RISK SCORE - a THIRD, separate 0-10 score, different in kind from
Score and Secondary Score: those measure "quality" (bullish vs bearish).
This measures "volatility/instability" (calm vs wild) - an axis where
neither end is inherently good or bad, just a different risk profile. Built
from 5 metrics that individually have no bullish/bearish direction (so none
of them could ever join the main Score or Secondary Score), but DO share a
common theme - see the column's own tooltip for the reasoning the user asked
for directly ("can directionless things be combined into a score?").

  1. Beta            - |beta| far from typical (~1) = more volatile than the
                        market, from fundamentals_data.tsv
  2. 52-Week Range    - how close the price sits to EITHER extreme (high or
     extremity          low) of its 52-week range - sitting near an extreme
                        is treated as "tension"/instability regardless of
                        which extreme, unlike Secondary Score's PEG/etc.
                        which have a clear cheap/expensive direction
  3. Volume Spike     - magnitude of the volume ratio alone, regardless of
     magnitude          price direction (Secondary/main Score already use
                        the same ratio WITH direction for a bullish/bearish
                        read - here only "how unusual" matters, not which way)
  4. Debt/Equity      - balance-sheet leverage - a highly-levered company is
                        more fragile/volatile under stress regardless of
                        whether its stock happens to be cheap or expensive
  5. Days-to-Cover     - short interest expressed in days of average volume
     (short squeeze)    needed to close all short positions - a high value
                        means a short squeeze could move the price sharply in
                        EITHER direction if shorts are forced to cover

Same design as the other two scores: each signal 0-2 points (missing data
gets neutral 1.0), summed to 0-10 raw (which already lands on the 0-10 scale
directly, unlike Secondary Score's 0-8), with an X/5 confidence count. HIGHER
= more volatile/unstable, not "worse" - read this score as a risk-tolerance
filter, not a quality signal.

Run: python compute_risk_score.py
Result: risk_score.tsv (TICKER, score, beta_pts, range_pts, vol_pts, debt_pts,
dtc_pts, confidence). A raw data file only - does NOT merge into all_rows.html
itself; the caller should call build_site.py once after all of a scan run's
raw-data writes are done (see build_site.py's docstring for why merging is
centralized there).
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
        if len(parts) != 32:
            continue

        def f(v):
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        data[parts[0]] = {
            "beta": f(parts[2]), "range52_pos": f(parts[13]), "volume_ratio": f(parts[10]),
            "debt_to_equity": f(parts[14]), "short_ratio": f(parts[15]),
        }
    return data


def score_beta_risk(beta):
    if beta is None:
        return None
    v = abs(beta)
    if v < 0.5:
        return 0.0
    if v < 0.8:
        return 0.5
    if v < 1.2:
        return 1.0
    if v < 1.8:
        return 1.5
    return 2.0


def score_range_risk(range52_pos):
    """Distance from the middle of the 52-week range (50%) - close to EITHER
    extreme (0% or 100%) is treated as more unstable/tense, not "bad"."""
    if range52_pos is None:
        return None
    distance = abs(range52_pos - 50)
    if distance < 15:
        return 0.0
    if distance < 30:
        return 0.5
    if distance < 40:
        return 1.0
    if distance < 47:
        return 1.5
    return 2.0


def score_volume_risk(volume_ratio):
    """Unlike Volume Spike's own coloring (which needs price direction),
    here only the MAGNITUDE of unusual activity matters - any big spike
    means more instability, regardless of which way price moved."""
    if volume_ratio is None:
        return None
    if volume_ratio < 1.5:
        return 0.0
    if volume_ratio < 2.5:
        return 1.0
    return 2.0


def score_debt_risk(debt_to_equity):
    """Yahoo's raw value is already a percentage (78.445 means 78.4%, i.e. a
    ratio of 0.78) - higher leverage means more balance-sheet fragility under
    stress, regardless of whether the stock itself looks cheap or expensive."""
    if debt_to_equity is None:
        return None
    v = abs(debt_to_equity)
    if v < 30:
        return 0.0
    if v < 80:
        return 0.5
    if v < 150:
        return 1.0
    if v < 250:
        return 1.5
    return 2.0


def score_days_to_cover_risk(short_ratio):
    """Days-to-cover: how many days of average volume it would take to close
    out every open short position. High values mean a short squeeze could
    move the price sharply if shorts are forced to buy back at once."""
    if short_ratio is None:
        return None
    if short_ratio < 1:
        return 0.0
    if short_ratio < 3:
        return 0.5
    if short_ratio < 6:
        return 1.0
    if short_ratio < 10:
        return 1.5
    return 2.0


def main():
    fundamentals = load_fundamentals()

    rows = []
    for ticker, fnd in fundamentals.items():
        beta_pts_raw = score_beta_risk(fnd.get("beta"))
        range_pts_raw = score_range_risk(fnd.get("range52_pos"))
        vol_pts_raw = score_volume_risk(fnd.get("volume_ratio"))
        debt_pts_raw = score_debt_risk(fnd.get("debt_to_equity"))
        dtc_pts_raw = score_days_to_cover_risk(fnd.get("short_ratio"))

        confidence = sum(
            x is not None for x in (beta_pts_raw, range_pts_raw, vol_pts_raw, debt_pts_raw, dtc_pts_raw)
        )
        if confidence == 0:
            continue

        beta_pts = beta_pts_raw if beta_pts_raw is not None else 1.0
        range_pts = range_pts_raw if range_pts_raw is not None else 1.0
        vol_pts = vol_pts_raw if vol_pts_raw is not None else 1.0
        debt_pts = debt_pts_raw if debt_pts_raw is not None else 1.0
        dtc_pts = dtc_pts_raw if dtc_pts_raw is not None else 1.0

        raw_total = beta_pts + range_pts + vol_pts + debt_pts + dtc_pts
        total = raw_total  # 5 signals * max 2 = 10, already on the 0-10 scale

        rows.append((ticker, total, beta_pts, range_pts, vol_pts, debt_pts, dtc_pts, confidence))

    with open(ROOT / "risk_score.tsv", "w", encoding="utf-8") as f:
        for ticker, total, beta_pts, range_pts, vol_pts, debt_pts, dtc_pts, confidence in rows:
            f.write(
                f"{ticker}\t{total:.1f}\t{beta_pts:.1f}\t{range_pts:.1f}\t{vol_pts:.1f}\t"
                f"{debt_pts:.1f}\t{dtc_pts:.1f}\t{confidence}\n"
            )

    print(f"Computed Risk Score for {len(rows)} tickers -> risk_score.tsv")


if __name__ == "__main__":
    main()
