"""
COMPUTE SECONDARY SCORE - a second, separate 0-10 score built from 6 "extra"
metrics that were each deliberately excluded from the main Score because none
of them has a clean, universal bullish/bearish direction on its own (P/E is
sector-dependent, Hedge Fund Activity's sample is only the ~3 default-shown
holders, Volume Spike needs price direction to mean anything, EPS Trend/Profit
Margin/Revenue Growth are fundamentals-quality signals that round out the
picture without displacing the main Score's more analyst/market-facing ones):

  1. P/E (TTM)          - cheap/expensive rule of thumb, from fundamentals_data.tsv
  2. Hedge Fund Activity - net Added vs Reduced among top holders, from hedge_fund_activity.tsv
  3. Volume Spike        - unusual volume + same-day price direction, from fundamentals_data.tsv
  4. EPS Trend           - whether analysts have been raising or cutting this
                           quarter's EPS estimate over the last 90 days, from
                           fundamentals_data.tsv/Yahoo's earningsTrend
  5. Profit Margin       - net profit margin %, from fundamentals_data.tsv/Yahoo's financialData
  6. Revenue Growth      - YoY revenue growth %, from fundamentals_data.tsv/Yahoo's financialData

This is explicitly a WEAKER heuristic than the main Score - combining
individually-shaky signals doesn't make them reliable, just averaged. It is
kept as a fully separate score (not blended into the main Score) so neither
one's meaning gets diluted - see the Secondary Score column's own tooltip.

Same design as the main Score: each signal is 0-2 points (missing data get a
neutral 1.0 rather than being excluded), summed to 0-12 raw, then scaled to
0-10 (raw * 10/12) so it reads on the same scale as the main Score. A
Confidence count (X/6) is tracked the same way too.

Run: python compute_secondary_score.py
Result: secondary_score.tsv (TICKER, score, pe_pts, hf_pts, vol_pts, eps_trend_pts,
margin_pts, growth_pts, confidence). A raw data file only - does NOT merge into
all_rows.html itself; the caller should call build_site.py once after all of a
scan run's raw-data writes are done (see build_site.py's docstring for why
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
        if len(parts) != 21:
            continue

        def f(v):
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        data[parts[0]] = {
            "pe": f(parts[3]), "volume_ratio": f(parts[10]), "price_change_pct": f(parts[11]),
            "peg": f(parts[12]), "eps_trend_pct": f(parts[17]),
            "profit_margins": f(parts[18]), "revenue_growth": f(parts[19]),
        }
    return data


def load_hedgefund():
    data = {}
    path = ROOT / "hedge_fund_activity.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 5:
            continue
        ticker, added, reduced, unchanged, total = parts
        data[ticker] = (int(added), int(reduced), int(total))
    return data


def score_pe(pe):
    if pe is None:
        return None
    if pe < 0:
        return 1.0  # loss-making - ratio is meaningless, not bad
    if pe < 10:
        return 2.0
    if pe < 15:
        return 1.5
    if pe < 25:
        return 1.0
    if pe < 40:
        return 0.5
    return 0.0


def score_peg(peg):
    """PEG (P/E divided by expected growth %) is a fairer version of the P/E
    check - it accounts for growth, so a high-P/E fast-growing company isn't
    unfairly penalized the way raw P/E would. Used INSTEAD of score_pe() when
    available (see main()), not in addition to it."""
    if peg is None:
        return None
    if peg < 0:
        return 1.0  # negative growth or negative earnings - ratio is not meaningful
    if peg < 1.0:
        return 2.0
    if peg < 1.5:
        return 1.5
    if peg < 2.5:
        return 1.0
    if peg < 4.0:
        return 0.5
    return 0.0


def score_hedgefund(hf):
    if hf is None:
        return None
    added, reduced, total = hf
    if total == 0:
        return None
    if added > reduced:
        return 2.0
    if reduced > added:
        return 0.0
    return 1.0


def score_eps_trend(eps_trend_pct):
    """Whether analysts have been raising or cutting their current-quarter EPS
    estimate over the last 90 days - a leading indicator of sentiment shift
    that often moves before the Rating itself catches up."""
    if eps_trend_pct is None:
        return None
    if eps_trend_pct > 5:
        return 2.0
    if eps_trend_pct > 1:
        return 1.5
    if eps_trend_pct > -1:
        return 1.0
    if eps_trend_pct > -5:
        return 0.5
    return 0.0


def score_profit_margin(profit_margins):
    """Yahoo's raw value is a fraction (0.276 = 27.6% net margin)."""
    if profit_margins is None:
        return None
    pct = profit_margins * 100
    if pct > 20:
        return 2.0
    if pct > 10:
        return 1.5
    if pct > 0:
        return 1.0
    if pct > -10:
        return 0.5
    return 0.0


def score_revenue_growth(revenue_growth):
    """Yahoo's raw value is a fraction (0.164 = 16.4% YoY growth)."""
    if revenue_growth is None:
        return None
    pct = revenue_growth * 100
    if pct > 20:
        return 2.0
    if pct > 10:
        return 1.5
    if pct > 0:
        return 1.0
    if pct > -10:
        return 0.5
    return 0.0


def score_volume(volume_ratio, price_change_pct):
    if volume_ratio is None:
        return None
    if volume_ratio < 2.0 or price_change_pct is None:
        return 1.0  # no real spike, or no price-direction data to interpret it - neutral
    if price_change_pct > 1:
        return 2.0 if volume_ratio >= 3.0 else 1.5
    if price_change_pct < -1:
        return 0.0 if volume_ratio >= 3.0 else 0.5
    return 1.0


def main():
    fundamentals = load_fundamentals()
    hedgefund = load_hedgefund()

    all_tickers = set(fundamentals) | set(hedgefund)
    rows = []
    for ticker in all_tickers:
        fnd = fundamentals.get(ticker, {})
        hf = hedgefund.get(ticker)

        # Prefer PEG over raw P/E when available - it's the fairer,
        # growth-adjusted version of the same "cheap vs expensive" question.
        peg_pts = score_peg(fnd.get("peg"))
        pe_pts_raw = peg_pts if peg_pts is not None else score_pe(fnd.get("pe"))
        hf_pts_raw = score_hedgefund(hf)
        vol_pts_raw = score_volume(fnd.get("volume_ratio"), fnd.get("price_change_pct"))
        eps_trend_pts_raw = score_eps_trend(fnd.get("eps_trend_pct"))
        margin_pts_raw = score_profit_margin(fnd.get("profit_margins"))
        growth_pts_raw = score_revenue_growth(fnd.get("revenue_growth"))

        confidence = sum(
            x is not None for x in
            (pe_pts_raw, hf_pts_raw, vol_pts_raw, eps_trend_pts_raw, margin_pts_raw, growth_pts_raw)
        )
        if confidence == 0:
            continue  # nothing at all to go on for this ticker - skip rather than show an all-neutral 5.0

        pe_pts = pe_pts_raw if pe_pts_raw is not None else 1.0
        hf_pts = hf_pts_raw if hf_pts_raw is not None else 1.0
        vol_pts = vol_pts_raw if vol_pts_raw is not None else 1.0
        eps_trend_pts = eps_trend_pts_raw if eps_trend_pts_raw is not None else 1.0
        margin_pts = margin_pts_raw if margin_pts_raw is not None else 1.0
        growth_pts = growth_pts_raw if growth_pts_raw is not None else 1.0

        raw_total = pe_pts + hf_pts + vol_pts + eps_trend_pts + margin_pts + growth_pts
        total = raw_total * 10 / 12

        rows.append((ticker, total, pe_pts, hf_pts, vol_pts, eps_trend_pts, margin_pts, growth_pts, confidence))

    with open(ROOT / "secondary_score.tsv", "w", encoding="utf-8") as f:
        for ticker, total, pe_pts, hf_pts, vol_pts, eps_trend_pts, margin_pts, growth_pts, confidence in rows:
            f.write(
                f"{ticker}\t{total:.1f}\t{pe_pts:.1f}\t{hf_pts:.1f}\t{vol_pts:.1f}\t"
                f"{eps_trend_pts:.1f}\t{margin_pts:.1f}\t{growth_pts:.1f}\t{confidence}\n"
            )

    print(f"Computed Secondary Score for {len(rows)} tickers -> secondary_score.tsv")


if __name__ == "__main__":
    main()
