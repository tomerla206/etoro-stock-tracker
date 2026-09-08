"""
COMPUTE SECONDARY SCORE - a second, separate 0-10 score built from 18 "extra"
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
  7. Gross Margin        - gross profit / revenue %, a pricing-power/moat
                           signal, from fundamentals_data.tsv/Yahoo's financialData
  8. Operating Margin    - operating income / revenue %, operational
                           efficiency, from fundamentals_data.tsv/Yahoo's financialData
  9. FCF Yield           - free cash flow as % of market cap, whether the
                           company generates real cash vs. just accounting
                           profit, from fundamentals_data.tsv/Yahoo's financialData
  10. Analyst Coverage   - number of analysts covering the stock - more
                           coverage means the Rating/Upside signals in the
                           main Score rest on a broader consensus, from
                           fundamentals_data.tsv/Yahoo's financialData
  11. Forward P/E vs TTM - whether the market expects earnings to improve
                           (forward P/E below trailing) or deteriorate
                           (forward P/E above trailing), from
                           fundamentals_data.tsv/Yahoo's defaultKeyStatistics
  12. P/B (Price-to-Book) - cheap/expensive vs. net asset value, a value
                           metric distinct from earnings-based P/E, from
                           fundamentals_data.tsv/Yahoo's defaultKeyStatistics
  13. EV/EBITDA           - valuation multiple that accounts for debt/cash on
                           the balance sheet, fairer across different capital
                           structures than P/E, from fundamentals_data.tsv/
                           Yahoo's defaultKeyStatistics
  14. EV/Revenue          - valuation multiple that still works when both
                           earnings AND EBITDA are negative, from
                           fundamentals_data.tsv/Yahoo's defaultKeyStatistics
  15. Dividend Payout Ratio - % of earnings paid as dividends - a sweet-spot
                           signal (too high risks a future dividend cut), from
                           fundamentals_data.tsv/Yahoo's summaryDetail
  16. EBITDA Margin        - profitability before financing/tax/D&A choices,
                           from fundamentals_data.tsv/Yahoo's financialData
  17. Cash-to-Market-Cap   - balance-sheet cash cushion already on hand
                           (distinct from FCF Yield's ongoing generation
                           rate), from fundamentals_data.tsv/Yahoo's
                           financialData
  18. OCF Margin           - operating cash flow / revenue, a cash-quality
                           check distinct from FCF Yield (nets out capex) and
                           Profit Margin (accounting, not cash), from
                           fundamentals_data.tsv/Yahoo's financialData

This is explicitly a WEAKER heuristic than the main Score - combining
individually-shaky signals doesn't make them reliable, just averaged. It is
kept as a fully separate score (not blended into the main Score) so neither
one's meaning gets diluted - see the Secondary Score column's own tooltip.

Same design as the main Score: each signal is 0-2 points (missing data get a
neutral 1.0 rather than being excluded), summed to 0-36 raw, then scaled to
0-10 (raw * 10/36) so it reads on the same scale as the main Score. A
Confidence count (X/18) is tracked the same way too.

Run: python compute_secondary_score.py
Result: secondary_score.tsv (TICKER, score, pe_pts, hf_pts, vol_pts, eps_trend_pts,
margin_pts, growth_pts, gross_margin_pts, op_margin_pts, fcf_yield_pts,
coverage_pts, fwd_pe_pts, pb_pts, ev_ebitda_pts, ev_revenue_pts, payout_pts,
ebitda_margin_pts, cash_mcap_pts, ocf_margin_pts, confidence). A raw data file
only - does NOT merge into
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
        if len(parts) != 45:
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
            "gross_margins": f(parts[26]), "operating_margins": f(parts[27]),
            "fcf_yield": f(parts[28]), "num_analyst_opinions": f(parts[30]),
            "forward_pe": f(parts[31]),
            "price_to_book": f(parts[32]), "ev_to_ebitda": f(parts[33]),
            "payout_ratio": f(parts[34]), "ev_to_revenue": f(parts[38]),
            "ebitda_margins": f(parts[39]), "cash_to_mcap": f(parts[40]),
            "ocf_margin": f(parts[41]),
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


def score_gross_margin(gross_margins):
    """Yahoo's raw value is a fraction (0.45 = 45% gross margin). Higher
    gross margin usually means pricing power / a competitive moat - a
    software company at 80% and a grocer at 25% aren't failing/succeeding
    relative to each other, but within a stock's own history a declining
    gross margin is a real quality warning."""
    if gross_margins is None:
        return None
    pct = gross_margins * 100
    if pct > 50:
        return 2.0
    if pct > 35:
        return 1.5
    if pct > 20:
        return 1.0
    if pct > 10:
        return 0.5
    return 0.0


def score_operating_margin(operating_margins):
    """Yahoo's raw value is a fraction (0.18 = 18% operating margin) -
    operating income / revenue, a read on operational efficiency distinct
    from the net Profit Margin signal already in this score (which also
    reflects tax/interest/one-off items operating margin excludes)."""
    if operating_margins is None:
        return None
    pct = operating_margins * 100
    if pct > 25:
        return 2.0
    if pct > 15:
        return 1.5
    if pct > 8:
        return 1.0
    if pct > 0:
        return 0.5
    return 0.0


def score_fcf_yield(fcf_yield):
    """Already computed as a percentage in fundamentals_scan.py (free cash
    flow / market cap * 100), unlike the fraction-valued Yahoo fields above.
    A company can report a healthy accounting profit while burning real
    cash (or vice versa) - this is the check for which one is actually true."""
    if fcf_yield is None:
        return None
    if fcf_yield > 8:
        return 2.0
    if fcf_yield > 5:
        return 1.5
    if fcf_yield > 2:
        return 1.0
    if fcf_yield > 0:
        return 0.5
    return 0.0


def score_analyst_coverage(num_analyst_opinions):
    """How many analysts actually cover this stock - not a bullish/bearish
    signal on its own, but a confidence check on the main Score's
    Rating/Upside signals: a 'Strong Buy' from 25 analysts rests on a much
    broader consensus than the same rating from just 2."""
    if num_analyst_opinions is None:
        return None
    n = num_analyst_opinions
    if n >= 20:
        return 2.0
    if n >= 10:
        return 1.5
    if n >= 5:
        return 1.0
    if n >= 1:
        return 0.5
    return 0.0


def score_forward_pe(pe, forward_pe):
    """Compares next year's expected P/E to today's trailing P/E - a forward
    P/E meaningfully BELOW trailing means the market expects earnings to
    grow (the same price divided by bigger expected earnings), while forward
    ABOVE trailing means expected deterioration. Only meaningful when both
    are positive (a loss-making trailing or forward year makes the ratio not
    comparable, same reasoning as score_pe()'s own negative-P/E handling)."""
    if pe is None or forward_pe is None or pe <= 0 or forward_pe <= 0:
        return None
    improvement_pct = (pe - forward_pe) / pe * 100
    if improvement_pct > 20:
        return 2.0
    if improvement_pct > 5:
        return 1.5
    if improvement_pct > -5:
        return 1.0
    if improvement_pct > -20:
        return 0.5
    return 0.0


def score_price_to_book(pb):
    """Price / book value per share - classic value metric, cheap/expensive
    rule of thumb like P/E but against net asset value instead of earnings.
    Negative book value (more liabilities than assets) is graded neutral,
    same reasoning as negative P/E - the ratio isn't meaningful there."""
    if pb is None:
        return None
    if pb < 0:
        return 1.0
    if pb < 1.0:
        return 2.0
    if pb < 3.0:
        return 1.5
    if pb < 6.0:
        return 1.0
    if pb < 10.0:
        return 0.5
    return 0.0


def score_ev_to_ebitda(ev_ebitda):
    """Enterprise Value / EBITDA - a valuation multiple that (unlike P/E)
    accounts for debt and cash on the balance sheet, so it's fairer when
    comparing companies with very different capital structures. Negative
    EBITDA (operating losses) is graded neutral - ratio not meaningful."""
    if ev_ebitda is None:
        return None
    if ev_ebitda < 0:
        return 1.0
    if ev_ebitda < 8:
        return 2.0
    if ev_ebitda < 14:
        return 1.5
    if ev_ebitda < 20:
        return 1.0
    if ev_ebitda < 30:
        return 0.5
    return 0.0


def score_ev_to_revenue(ev_revenue):
    """Enterprise Value / Revenue - the valuation multiple that still works
    when a company has negative earnings AND negative EBITDA (common for
    early-stage growth companies where neither P/E nor EV/EBITDA apply)."""
    if ev_revenue is None:
        return None
    if ev_revenue < 0:
        return 1.0
    if ev_revenue < 2:
        return 2.0
    if ev_revenue < 5:
        return 1.5
    if ev_revenue < 10:
        return 1.0
    if ev_revenue < 20:
        return 0.5
    return 0.0


def score_payout_ratio(payout_ratio):
    """% of earnings paid out as dividends. A SWEET SPOT, not "higher is
    better": near 0 means no dividend (not necessarily bad, but nothing to
    reward here), a moderate payout is sustainable, and a payout above 100%
    means the company is paying out more than it earns - a dividend cut risk."""
    if payout_ratio is None:
        return None
    pct = payout_ratio * 100
    if pct <= 0:
        return 1.0
    if pct < 60:
        return 2.0
    if pct < 80:
        return 1.5
    if pct < 100:
        return 1.0
    return 0.0


def score_ebitda_margin(ebitda_margins):
    """Yahoo's raw value is a fraction. EBITDA margin sits between Gross and
    Operating margin - profitability before the effect of financing/tax
    decisions AND before depreciation/amortization choices."""
    if ebitda_margins is None:
        return None
    pct = ebitda_margins * 100
    if pct > 35:
        return 2.0
    if pct > 20:
        return 1.5
    if pct > 10:
        return 1.0
    if pct > 0:
        return 0.5
    return 0.0


def score_cash_to_mcap(cash_to_mcap):
    """Already a percentage (total cash / market cap * 100, computed in
    fundamentals_scan.py). A balance-sheet cushion signal distinct from FCF
    Yield - this is the stockpile already on hand, not the ongoing rate of
    cash generation."""
    if cash_to_mcap is None:
        return None
    if cash_to_mcap > 20:
        return 2.0
    if cash_to_mcap > 10:
        return 1.5
    if cash_to_mcap > 5:
        return 1.0
    if cash_to_mcap > 1:
        return 0.5
    return 0.0


def score_ocf_margin(ocf_margin):
    """Already a percentage (operating cash flow / revenue * 100, computed
    in fundamentals_scan.py). A cash-quality check distinct from FCF Yield
    (which nets out capex) and Profit Margin (accounting profit, not cash) -
    catches a company reporting healthy profit that isn't actually
    collecting the cash behind it."""
    if ocf_margin is None:
        return None
    if ocf_margin > 25:
        return 2.0
    if ocf_margin > 15:
        return 1.5
    if ocf_margin > 5:
        return 1.0
    if ocf_margin > 0:
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
        gross_margin_pts_raw = score_gross_margin(fnd.get("gross_margins"))
        op_margin_pts_raw = score_operating_margin(fnd.get("operating_margins"))
        fcf_yield_pts_raw = score_fcf_yield(fnd.get("fcf_yield"))
        coverage_pts_raw = score_analyst_coverage(fnd.get("num_analyst_opinions"))
        fwd_pe_pts_raw = score_forward_pe(fnd.get("pe"), fnd.get("forward_pe"))
        pb_pts_raw = score_price_to_book(fnd.get("price_to_book"))
        ev_ebitda_pts_raw = score_ev_to_ebitda(fnd.get("ev_to_ebitda"))
        ev_revenue_pts_raw = score_ev_to_revenue(fnd.get("ev_to_revenue"))
        payout_pts_raw = score_payout_ratio(fnd.get("payout_ratio"))
        ebitda_margin_pts_raw = score_ebitda_margin(fnd.get("ebitda_margins"))
        cash_mcap_pts_raw = score_cash_to_mcap(fnd.get("cash_to_mcap"))
        ocf_margin_pts_raw = score_ocf_margin(fnd.get("ocf_margin"))

        confidence = sum(
            x is not None for x in
            (pe_pts_raw, hf_pts_raw, vol_pts_raw, eps_trend_pts_raw, margin_pts_raw, growth_pts_raw,
             gross_margin_pts_raw, op_margin_pts_raw, fcf_yield_pts_raw, coverage_pts_raw, fwd_pe_pts_raw,
             pb_pts_raw, ev_ebitda_pts_raw, ev_revenue_pts_raw, payout_pts_raw,
             ebitda_margin_pts_raw, cash_mcap_pts_raw, ocf_margin_pts_raw)
        )
        if confidence == 0:
            continue  # nothing at all to go on for this ticker - skip rather than show an all-neutral 5.0

        pe_pts = pe_pts_raw if pe_pts_raw is not None else 1.0
        hf_pts = hf_pts_raw if hf_pts_raw is not None else 1.0
        vol_pts = vol_pts_raw if vol_pts_raw is not None else 1.0
        eps_trend_pts = eps_trend_pts_raw if eps_trend_pts_raw is not None else 1.0
        margin_pts = margin_pts_raw if margin_pts_raw is not None else 1.0
        growth_pts = growth_pts_raw if growth_pts_raw is not None else 1.0
        gross_margin_pts = gross_margin_pts_raw if gross_margin_pts_raw is not None else 1.0
        op_margin_pts = op_margin_pts_raw if op_margin_pts_raw is not None else 1.0
        fcf_yield_pts = fcf_yield_pts_raw if fcf_yield_pts_raw is not None else 1.0
        coverage_pts = coverage_pts_raw if coverage_pts_raw is not None else 1.0
        fwd_pe_pts = fwd_pe_pts_raw if fwd_pe_pts_raw is not None else 1.0
        pb_pts = pb_pts_raw if pb_pts_raw is not None else 1.0
        ev_ebitda_pts = ev_ebitda_pts_raw if ev_ebitda_pts_raw is not None else 1.0
        ev_revenue_pts = ev_revenue_pts_raw if ev_revenue_pts_raw is not None else 1.0
        payout_pts = payout_pts_raw if payout_pts_raw is not None else 1.0
        ebitda_margin_pts = ebitda_margin_pts_raw if ebitda_margin_pts_raw is not None else 1.0
        cash_mcap_pts = cash_mcap_pts_raw if cash_mcap_pts_raw is not None else 1.0
        ocf_margin_pts = ocf_margin_pts_raw if ocf_margin_pts_raw is not None else 1.0

        raw_total = (pe_pts + hf_pts + vol_pts + eps_trend_pts + margin_pts + growth_pts
                     + gross_margin_pts + op_margin_pts + fcf_yield_pts + coverage_pts + fwd_pe_pts
                     + pb_pts + ev_ebitda_pts + ev_revenue_pts + payout_pts
                     + ebitda_margin_pts + cash_mcap_pts + ocf_margin_pts)
        total = raw_total * 10 / 36

        rows.append((ticker, total, pe_pts, hf_pts, vol_pts, eps_trend_pts, margin_pts, growth_pts,
                     gross_margin_pts, op_margin_pts, fcf_yield_pts, coverage_pts, fwd_pe_pts,
                     pb_pts, ev_ebitda_pts, ev_revenue_pts, payout_pts, ebitda_margin_pts,
                     cash_mcap_pts, ocf_margin_pts, confidence))

    with open(ROOT / "secondary_score.tsv", "w", encoding="utf-8") as f:
        for (ticker, total, pe_pts, hf_pts, vol_pts, eps_trend_pts, margin_pts, growth_pts,
             gross_margin_pts, op_margin_pts, fcf_yield_pts, coverage_pts, fwd_pe_pts,
             pb_pts, ev_ebitda_pts, ev_revenue_pts, payout_pts, ebitda_margin_pts,
             cash_mcap_pts, ocf_margin_pts, confidence) in rows:
            f.write(
                f"{ticker}\t{total:.1f}\t{pe_pts:.1f}\t{hf_pts:.1f}\t{vol_pts:.1f}\t"
                f"{eps_trend_pts:.1f}\t{margin_pts:.1f}\t{growth_pts:.1f}\t"
                f"{gross_margin_pts:.1f}\t{op_margin_pts:.1f}\t{fcf_yield_pts:.1f}\t"
                f"{coverage_pts:.1f}\t{fwd_pe_pts:.1f}\t{pb_pts:.1f}\t{ev_ebitda_pts:.1f}\t"
                f"{ev_revenue_pts:.1f}\t{payout_pts:.1f}\t{ebitda_margin_pts:.1f}\t"
                f"{cash_mcap_pts:.1f}\t{ocf_margin_pts:.1f}\t{confidence}\n"
            )

    print(f"Computed Secondary Score for {len(rows)} tickers -> secondary_score.tsv")


if __name__ == "__main__":
    main()
