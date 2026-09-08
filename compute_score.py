"""
COMPUTE SCORE - combines 15 independent signals into one 1-10 composite Score
per ticker:

  1. Analyst Rating      (Strong Buy .. Strong Sell, from consensus_ratings.txt)
  2. Analyst Upside %    (avg price target vs current price, from analyst_targets_*.txt)
  3. Insider Activity    (net $ bought/sold last 30d, from insider_activity.tsv)
  4. Short Interest      (% of float short, from fundamentals_data.tsv)
  5. Technicals          (RSI14 + price vs 50/200-day MA, from fundamentals_data.tsv)
  6. Analyst Dispersion  (Low-High target spread relative to Avg - tight spread
                          means analysts agree, from analyst_targets_*.txt)
  7. Earnings Surprise   (avg beat/miss % over the last few reported quarters,
                          from fundamentals_data.tsv/Yahoo's earningsHistory)
  8. Rating Trend        (change in analysts' average recommendation over the
                          last 3 months - upgrades vs downgrades - from
                          fundamentals_data.tsv/Yahoo's recommendationTrend)
  9. Return on Equity    (net income / shareholder equity - how efficiently
                          the company turns equity into profit, from
                          fundamentals_data.tsv/Yahoo's financialData)
  10. Institutional Ownership (% of shares held by institutions - a rough
                          "smart money" confidence signal, from
                          fundamentals_data.tsv/Yahoo's defaultKeyStatistics)
  11. Current Ratio      (current assets / current liabilities - short-term
                          liquidity health, from fundamentals_data.tsv/Yahoo's
                          financialData)
  12. Quick Ratio        (like Current Ratio but excludes inventory - a
                          stricter near-term liquidity test, from
                          fundamentals_data.tsv/Yahoo's financialData)
  13. Return on Assets   (net income / total assets - profitability that,
                          unlike ROE, isn't inflated by leverage/buybacks,
                          from fundamentals_data.tsv/Yahoo's financialData)
  14. Held % Insiders    (% of shares held by company insiders - management
                          with real skin in the game, from
                          fundamentals_data.tsv/Yahoo's defaultKeyStatistics)
  15. Relative Strength  (52-week price change vs. the S&P 500 over the same
                          window - isolates stock-specific performance from
                          the market's own move, from fundamentals_data.tsv/
                          Yahoo's defaultKeyStatistics)

Each signal is scored 0-2 points (2 = most bullish), summed (max 30) and
scaled to 0-10. This is a transparent, hand-picked heuristic, not a
statistically fitted model - the bucket thresholds below are the whole
"methodology" and are deliberately simple so they can be explained in a
tooltip on the site. A ticker missing a given signal gets 1.0 (neutral) for
that signal rather than being excluded, so partial data still produces a
usable Score instead of dragging it to zero.

Run: python compute_score.py
Result: score.tsv (TICKER, score, rating_pts, upside_pts, insider_pts, short_pts,
tech_pts, dispersion_pts, surprise_pts, rating_trend_pts, roe_pts, inst_own_pts,
current_ratio_pts, quick_ratio_pts, roa_pts, held_insiders_pts,
relative_strength_pts, confidence). A raw data file only - does
NOT merge into all_rows.html itself, and does NOT call score_history.py itself
either (that needs both this AND compute_secondary_score.py's output, so the
caller runs it once after both - see score_history.py's own docstring). The
caller should call build_site.py once after all of a scan run's raw-data writes
are done (see build_site.py's docstring for why merging is centralized there).
"""

import glob
from pathlib import Path

ROOT = Path(__file__).parent

RATING_POINTS = {
    "Strong Buy": 2.0, "Moderate Buy": 1.5, "Hold": 1.0,
    "Moderate Sell": 0.5, "Strong Sell": 0.0,
}


def load_analyst_data():
    """ticker -> (price, avg_target, status, low_target, high_target)"""
    data = {}
    files = sorted(f for f in glob.glob(str(ROOT / "analyst_targets_*.txt")) if "_OLD" not in f)
    for fname in files:
        for line in Path(fname).read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != 8:
                continue
            ticker, name, price, low, avg, high, status, trade = parts

            def f(v):
                try:
                    return float(v) if v else None
                except ValueError:
                    return None

            data[ticker] = (f(price), f(avg), status, f(low), f(high))
    return data


def load_consensus_ratings():
    data = {}
    path = ROOT / "consensus_ratings.txt"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            data[parts[0]] = parts[2]
    return data


def load_insider():
    data = {}
    path = ROOT / "insider_activity.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) == 6:
            try:
                data[parts[0]] = float(parts[1])
            except ValueError:
                pass
    return data


def load_fundamentals():
    data = {}
    path = ROOT / "fundamentals_data.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 45:
            continue
        (ticker, short_pct, beta, pe, rsi14, price, ma50, ma200, market_cap, market_cap_fmt,
         volume_ratio, price_change_pct, peg, range52_pos,
         debt_to_equity, short_ratio, earnings_surprise_avg, eps_trend_pct,
         profit_margins, revenue_growth, rating_trend_delta,
         return_on_equity, current_ratio, institutional_ownership,
         quick_ratio, return_on_assets, gross_margins, operating_margins,
         fcf_yield, held_pct_insiders, num_analyst_opinions, forward_pe,
         price_to_book, ev_to_ebitda, payout_ratio, eps_growth_5y,
         relative_strength_52w, short_interest_trend_pct, ev_to_revenue,
         ebitda_margins, cash_to_mcap, ocf_margin, earnings_quarterly_growth,
         eps_growth_next_year, float_pct) = parts

        def f(v):
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        data[ticker] = {
            "short_pct": f(short_pct), "beta": f(beta), "pe": f(pe),
            "rsi14": f(rsi14), "price": f(price), "ma50": f(ma50), "ma200": f(ma200),
            "market_cap": f(market_cap), "market_cap_fmt": market_cap_fmt if market_cap_fmt != "None" else None,
            "earnings_surprise_avg": f(earnings_surprise_avg),
            "rating_trend_delta": f(rating_trend_delta),
            "return_on_equity": f(return_on_equity), "current_ratio": f(current_ratio),
            "institutional_ownership": f(institutional_ownership),
            "quick_ratio": f(quick_ratio), "return_on_assets": f(return_on_assets),
            "gross_margins": f(gross_margins), "operating_margins": f(operating_margins),
            "fcf_yield": f(fcf_yield), "held_pct_insiders": f(held_pct_insiders),
            "num_analyst_opinions": f(num_analyst_opinions), "forward_pe": f(forward_pe),
            "relative_strength_52w": f(relative_strength_52w),
        }
    return data


def score_rating(rating):
    if rating is None:
        return 1.0
    return RATING_POINTS.get(rating, 1.0)


def score_upside(price, avg_target):
    if not price or not avg_target:
        return 1.0
    upside_pct = (avg_target - price) / price * 100
    if upside_pct > 20:
        return 2.0
    if upside_pct > 5:
        return 1.5
    if upside_pct > -5:
        return 1.0
    if upside_pct > -20:
        return 0.5
    return 0.0


def score_insider(net, market_cap):
    """Normalized by market cap, not raw dollars - a $1.8M sale is noise for a
    $4T company (AAPL: ratio ~0.00004%) but a real signal for a $50M one
    (ratio ~3.6%). Without this, mega-caps' routine RSU-vesting sales scored
    identically to a small-cap insider's high-conviction dump."""
    if net is None or net == 0:
        return 1.0
    if not market_cap:
        return 2.0 if net > 0 else 0.7  # no market cap on file - fall back to the old flat scoring
    ratio = abs(net) / market_cap
    if net > 0:
        if ratio >= 0.001:
            return 2.0
        if ratio >= 0.0001:
            return 1.7
        return 1.3
    else:
        if ratio >= 0.001:
            return 0.3
        if ratio >= 0.0001:
            return 0.7
        return 1.0


def score_short_interest(short_pct):
    if short_pct is None:
        return 1.0
    pct = short_pct * 100  # raw is a fraction (0.008 = 0.8%)
    if pct < 2:
        return 2.0
    if pct < 5:
        return 1.5
    if pct < 10:
        return 1.0
    if pct < 20:
        return 0.5
    return 0.0


def score_dispersion(low, high, avg):
    """How tightly analysts agree on the target - a narrow Low-High spread
    (relative to the average target) means the Street sees this stock's fair
    value clearly, while a wide spread means analysts are guessing wildly.
    Tight agreement is treated as bullish-leaning here (more conviction behind
    the same Upside % number the Score already counts separately)."""
    if not low or not high or not avg:
        return 1.0
    spread_pct = (high - low) / avg * 100
    if spread_pct < 20:
        return 2.0
    if spread_pct < 40:
        return 1.5
    if spread_pct < 70:
        return 1.0
    if spread_pct < 100:
        return 0.5
    return 0.0


def score_earnings_surprise(avg_surprise_pct):
    """Average earnings beat/miss % over Yahoo's last few reported quarters -
    a consistent history of beating estimates is a quality signal distinct
    from the forward-looking analyst Rating/Upside signals above."""
    if avg_surprise_pct is None:
        return 1.0
    if avg_surprise_pct > 10:
        return 2.0
    if avg_surprise_pct > 2:
        return 1.5
    if avg_surprise_pct > -2:
        return 1.0
    if avg_surprise_pct > -10:
        return 0.5
    return 0.0


def score_rating_trend(rating_trend_delta):
    """Change in analysts' average recommendation (1=Strong Sell..5=Strong Buy)
    over the last 3 months - this catches upgrade/downgrade momentum that the
    static current Rating snapshot alone can't show (a Rating of "Hold" looks
    identical whether it was just downgraded from Buy or just upgraded from
    Sell, even though those are opposite signals)."""
    if rating_trend_delta is None:
        return 1.0
    if rating_trend_delta > 0.15:
        return 2.0
    if rating_trend_delta > 0.05:
        return 1.5
    if rating_trend_delta > -0.05:
        return 1.0
    if rating_trend_delta > -0.15:
        return 0.5
    return 0.0


def score_roe(return_on_equity):
    """Yahoo's raw value is a fraction (1.4875 = 148.75% for AAPL, inflated
    by buybacks shrinking equity - extreme values still just mean "very
    efficient at turning equity into profit", not penalized here)."""
    if return_on_equity is None:
        return 1.0
    pct = return_on_equity * 100
    if pct > 25:
        return 2.0
    if pct > 15:
        return 1.5
    if pct > 5:
        return 1.0
    if pct > 0:
        return 0.5
    return 0.0


def score_institutional_ownership(institutional_ownership):
    """Yahoo's raw value is a fraction (0.664 = 66.4% held by institutions).
    Higher = more "smart money" confidence backing the stock."""
    if institutional_ownership is None:
        return 1.0
    pct = institutional_ownership * 100
    if pct > 70:
        return 2.0
    if pct > 50:
        return 1.5
    if pct > 30:
        return 1.0
    if pct > 10:
        return 0.5
    return 0.0


def score_current_ratio(current_ratio):
    """Current assets / current liabilities - short-term liquidity health.
    Unlike the other signals here, this has a SWEET SPOT rather than
    "higher is always better": below 1.0 means the company may struggle to
    cover its near-term bills; above ~3.0 usually means too much cash is
    sitting idle instead of being put to work."""
    if current_ratio is None:
        return 1.0
    if current_ratio < 1.0:
        return 0.0
    if current_ratio < 1.5:
        return 1.0
    if current_ratio <= 3.0:
        return 2.0
    return 1.0


def score_quick_ratio(quick_ratio):
    """(current assets - inventory) / current liabilities - stricter than
    Current Ratio since it excludes inventory (which may not convert to cash
    quickly). Naturally runs lower than Current Ratio, so the sweet-spot
    thresholds are scaled down accordingly - same non-monotonic shape
    (too low is a liquidity risk, too high just means idle cash)."""
    if quick_ratio is None:
        return 1.0
    if quick_ratio < 0.5:
        return 0.0
    if quick_ratio < 1.0:
        return 1.0
    if quick_ratio <= 2.0:
        return 2.0
    return 1.0


def score_roa(return_on_assets):
    """Net income / total assets. Unlike ROE, not inflated by leverage or
    buybacks shrinking the equity base - a company can have a sky-high ROE
    from debt alone while ROA stays modest, so this is a cleaner read on how
    efficiently the underlying assets generate profit. Runs much lower than
    ROE (double-digit ROA is already very strong), so thresholds are scaled
    down accordingly."""
    if return_on_assets is None:
        return 1.0
    pct = return_on_assets * 100
    if pct > 15:
        return 2.0
    if pct > 8:
        return 1.5
    if pct > 2:
        return 1.0
    if pct > 0:
        return 0.5
    return 0.0


def score_held_insiders(held_pct_insiders):
    """% of shares held by company insiders (management/board) - unlike
    Institutional Ownership this isn't "smart money" following the stock,
    it's the people running the company having real skin in the game.
    Naturally much lower than institutional ownership (a handful of
    executives vs. every fund combined), so thresholds are scaled down."""
    if held_pct_insiders is None:
        return 1.0
    pct = held_pct_insiders * 100
    if pct > 20:
        return 2.0
    if pct > 10:
        return 1.5
    if pct > 5:
        return 1.0
    if pct > 1:
        return 0.5
    return 0.0


def score_relative_strength(relative_strength_52w):
    """The stock's own 52-week % change minus the S&P 500's over the same
    window (already computed as percentage-point difference in
    fundamentals_scan.py). "Up 15%" means very different things depending on
    whether the market was up 5% (real outperformance) or up 25% (quietly
    lagging) - this isolates the stock-specific component."""
    if relative_strength_52w is None:
        return 1.0
    if relative_strength_52w > 20:
        return 2.0
    if relative_strength_52w > 5:
        return 1.5
    if relative_strength_52w > -5:
        return 1.0
    if relative_strength_52w > -20:
        return 0.5
    return 0.0


def score_technicals(price, ma50, ma200, rsi14):
    if price is None and rsi14 is None:
        return 1.0
    pts = 1.0
    if price is not None and ma50 is not None:
        pts += 0.5 if price > ma50 else -0.5
    if price is not None and ma200 is not None:
        pts += 0.5 if price > ma200 else -0.5
    if rsi14 is not None and rsi14 > 70:
        pts -= 0.5
    return max(0.0, min(2.0, pts))


def main():
    analyst = load_analyst_data()
    ratings = load_consensus_ratings()
    insider = load_insider()
    fundamentals = load_fundamentals()

    rows = []
    for ticker, (price, avg_target, status, low_target, high_target) in analyst.items():
        if status not in ("OK", "CVR"):
            continue  # no analyst coverage at all - Score would be meaningless
        fnd = fundamentals.get(ticker, {})
        rating = ratings.get(ticker)
        net = insider.get(ticker)
        short_pct = fnd.get("short_pct")
        tech_price = fnd.get("price") or price
        ma50, ma200, rsi14 = fnd.get("ma50"), fnd.get("ma200"), fnd.get("rsi14")
        surprise = fnd.get("earnings_surprise_avg")
        rating_trend_delta = fnd.get("rating_trend_delta")
        return_on_equity = fnd.get("return_on_equity")
        institutional_ownership = fnd.get("institutional_ownership")
        current_ratio = fnd.get("current_ratio")
        quick_ratio = fnd.get("quick_ratio")
        return_on_assets = fnd.get("return_on_assets")
        held_pct_insiders = fnd.get("held_pct_insiders")
        relative_strength_52w = fnd.get("relative_strength_52w")

        rating_pts = score_rating(rating)
        upside_pts = score_upside(price, avg_target)
        insider_pts = score_insider(net, fnd.get("market_cap"))
        short_pts = score_short_interest(short_pct)
        tech_pts = score_technicals(tech_price, ma50, ma200, rsi14)
        dispersion_pts = score_dispersion(low_target, high_target, avg_target)
        surprise_pts = score_earnings_surprise(surprise)
        rating_trend_pts = score_rating_trend(rating_trend_delta)
        roe_pts = score_roe(return_on_equity)
        inst_own_pts = score_institutional_ownership(institutional_ownership)
        current_ratio_pts = score_current_ratio(current_ratio)
        quick_ratio_pts = score_quick_ratio(quick_ratio)
        roa_pts = score_roa(return_on_assets)
        held_insiders_pts = score_held_insiders(held_pct_insiders)
        relative_strength_pts = score_relative_strength(relative_strength_52w)

        # Confidence: how many of the 11 signals were REAL data vs. a neutral
        # default because the signal was missing. A 7.0 built from 11 real
        # signals and a 7.0 built from 2 real + 9 defaults are not equally
        # trustworthy, even though the number looks the same - see the
        # Score column's tooltip for how this is surfaced on screen.
        confidence = sum([
            rating is not None,
            price is not None and avg_target is not None,
            net is not None,
            short_pct is not None,
            tech_price is not None and (ma50 is not None or ma200 is not None or rsi14 is not None),
            bool(low_target and high_target and avg_target),
            surprise is not None,
            rating_trend_delta is not None,
            return_on_equity is not None,
            institutional_ownership is not None,
            current_ratio is not None,
            quick_ratio is not None,
            return_on_assets is not None,
            held_pct_insiders is not None,
            relative_strength_52w is not None,
        ])

        raw_total = (rating_pts + upside_pts + insider_pts + short_pts + tech_pts
                     + dispersion_pts + surprise_pts + rating_trend_pts
                     + roe_pts + inst_own_pts + current_ratio_pts
                     + quick_ratio_pts + roa_pts + held_insiders_pts + relative_strength_pts)
        total = raw_total * 10 / 30
        rows.append((ticker, total, rating_pts, upside_pts, insider_pts, short_pts, tech_pts,
                     dispersion_pts, surprise_pts, rating_trend_pts,
                     roe_pts, inst_own_pts, current_ratio_pts,
                     quick_ratio_pts, roa_pts, held_insiders_pts, relative_strength_pts, confidence))

    with open(ROOT / "score.tsv", "w", encoding="utf-8") as f:
        for (ticker, total, r, u, i, s, t, disp, surp, rtrend, roe, iown, curr,
             quickr, roa, heldins, relstr, confidence) in rows:
            f.write(
                f"{ticker}\t{total:.1f}\t{r:.1f}\t{u:.1f}\t{i:.1f}\t{s:.1f}\t{t:.1f}\t"
                f"{disp:.1f}\t{surp:.1f}\t{rtrend:.1f}\t{roe:.1f}\t{iown:.1f}\t{curr:.1f}\t"
                f"{quickr:.1f}\t{roa:.1f}\t{heldins:.1f}\t{relstr:.1f}\t{confidence}\n"
            )

    print(f"Computed Score for {len(rows)} tickers -> score.tsv")


if __name__ == "__main__":
    main()
