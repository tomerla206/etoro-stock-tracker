"""
SCORE HISTORY - appends a dated snapshot of every ticker's Score AND
Secondary Score - including each score's individual component points, not
just the totals - (+ the price they were computed against) to
score_history.tsv, one row per ticker per day.

Why this exists: a real backtest of either score's formula needs point-in-time
historical values for their inputs (Rating, Insider $, Short Interest, PEG,
Hedge Fund Activity, etc.), which none of the free sources (TipRanks/SEC/
Yahoo) expose retroactively - only their current state. So instead of
backtesting the past, this starts forward-testing from today: once enough
daily snapshots accumulate (a few months), a future session can join
score_history.tsv against later price data and ask not just "did tickers
with Score >= 7 on day X outperform Score <= 4 by day X+30/X+90?" but also
"which INDIVIDUAL component (Rating? Insider? Short Interest?) actually
correlated with the outcome, and which ones were dead weight?" - the
per-component columns are what make that second, more useful question
answerable later. See REFRESH_METHOD.md.

Run this AFTER BOTH compute_score.py AND compute_secondary_score.py (it reads
score.tsv, secondary_score.tsv, and fundamentals_data.tsv - all three must
already exist for this run to capture both scores together, not one stale and
one fresh). Idempotent per day: re-running on the same date replaces that
date's rows instead of duplicating them, so accidentally running FUNDAMENTALS
SCAN twice in one day doesn't skew the history with two data points for the
same day.

Adding a future third score: add a load_<name>() function following
load_secondary_score()'s shape (return the total, confidence, AND each
component), add its columns to HISTORY_COLUMNS and the write loop below - the
column list is the single source of truth for the file's shape.

Result: score_history.tsv, columns per HISTORY_COLUMNS below - date, ticker,
price, then Score's total/confidence/15 components, then Secondary Score's
total/confidence/18 components, then Risk Score's total/confidence/7
components, then Growth Score's total/confidence/3 components, then Overall
Score's total/confidence (no separate components - it's a blend of Score and
Secondary Score's totals, not an independent set of signals).
"""

import datetime
from pathlib import Path

ROOT = Path(__file__).parent
HISTORY_FILE = ROOT / "score_history.tsv"

HISTORY_COLUMNS = [
    "date", "ticker", "price",
    "score", "score_confidence", "score_rating_pts", "score_upside_pts",
    "score_insider_pts", "score_short_pts", "score_tech_pts",
    "score_dispersion_pts", "score_surprise_pts", "score_ratingtrend_pts",
    "score_roe_pts", "score_instown_pts", "score_currentratio_pts",
    "score_quickratio_pts", "score_roa_pts", "score_heldinsiders_pts", "score_relstrength_pts",
    "secscore", "secscore_confidence", "secscore_pe_pts", "secscore_hf_pts", "secscore_vol_pts",
    "secscore_epstrend_pts", "secscore_margin_pts", "secscore_growth_pts",
    "secscore_grossmargin_pts", "secscore_opmargin_pts", "secscore_fcfyield_pts",
    "secscore_coverage_pts", "secscore_fwdpe_pts",
    "secscore_pb_pts", "secscore_evebitda_pts", "secscore_evrevenue_pts", "secscore_payout_pts",
    "secscore_ebitdamargin_pts", "secscore_cashmcap_pts", "secscore_ocfmargin_pts",
    "riskscore", "riskscore_confidence", "riskscore_beta_pts", "riskscore_range_pts", "riskscore_vol_pts",
    "riskscore_debt_pts", "riskscore_dtc_pts", "riskscore_shorttrend_pts", "riskscore_float_pts",
    "growthscore", "growthscore_confidence", "growthscore_quarterly_pts",
    "growthscore_nextyear_pts", "growthscore_fiveyear_pts",
    "overallscore", "overallscore_confidence",
]


def load_score():
    """ticker -> dict of total/confidence/component points"""
    data = {}
    path = ROOT / "score.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 18:
            continue
        (ticker, total, rating, upside, insider, short, tech, dispersion, surprise,
         rating_trend, roe, inst_own, current_ratio, quick_ratio, roa, held_insiders,
         relative_strength, confidence) = parts
        data[ticker] = {
            "score": total, "score_confidence": confidence,
            "score_rating_pts": rating, "score_upside_pts": upside,
            "score_insider_pts": insider, "score_short_pts": short, "score_tech_pts": tech,
            "score_dispersion_pts": dispersion, "score_surprise_pts": surprise,
            "score_ratingtrend_pts": rating_trend,
            "score_roe_pts": roe, "score_instown_pts": inst_own, "score_currentratio_pts": current_ratio,
            "score_quickratio_pts": quick_ratio, "score_roa_pts": roa,
            "score_heldinsiders_pts": held_insiders, "score_relstrength_pts": relative_strength,
        }
    return data


def load_secondary_score():
    """ticker -> dict of total/confidence/component points"""
    data = {}
    path = ROOT / "secondary_score.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 21:
            continue
        (ticker, total, pe_pts, hf_pts, vol_pts, eps_trend_pts, margin_pts, growth_pts,
         gross_margin_pts, op_margin_pts, fcf_yield_pts, coverage_pts, fwd_pe_pts,
         pb_pts, ev_ebitda_pts, ev_revenue_pts, payout_pts, ebitda_margin_pts,
         cash_mcap_pts, ocf_margin_pts, confidence) = parts
        data[ticker] = {
            "secscore": total, "secscore_confidence": confidence,
            "secscore_pe_pts": pe_pts, "secscore_hf_pts": hf_pts, "secscore_vol_pts": vol_pts,
            "secscore_epstrend_pts": eps_trend_pts,
            "secscore_margin_pts": margin_pts, "secscore_growth_pts": growth_pts,
            "secscore_grossmargin_pts": gross_margin_pts, "secscore_opmargin_pts": op_margin_pts,
            "secscore_fcfyield_pts": fcf_yield_pts, "secscore_coverage_pts": coverage_pts,
            "secscore_fwdpe_pts": fwd_pe_pts,
            "secscore_pb_pts": pb_pts, "secscore_evebitda_pts": ev_ebitda_pts,
            "secscore_evrevenue_pts": ev_revenue_pts, "secscore_payout_pts": payout_pts,
            "secscore_ebitdamargin_pts": ebitda_margin_pts, "secscore_cashmcap_pts": cash_mcap_pts,
            "secscore_ocfmargin_pts": ocf_margin_pts,
        }
    return data


def load_risk_score():
    """ticker -> dict of total/confidence/component points"""
    data = {}
    path = ROOT / "risk_score.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 10:
            continue
        (ticker, total, beta_pts, range_pts, vol_pts, debt_pts, dtc_pts,
         short_trend_pts, float_pts, confidence) = parts
        data[ticker] = {
            "riskscore": total, "riskscore_confidence": confidence,
            "riskscore_beta_pts": beta_pts, "riskscore_range_pts": range_pts, "riskscore_vol_pts": vol_pts,
            "riskscore_debt_pts": debt_pts, "riskscore_dtc_pts": dtc_pts,
            "riskscore_shorttrend_pts": short_trend_pts, "riskscore_float_pts": float_pts,
        }
    return data


def load_growth_score():
    """ticker -> dict of total/confidence/component points"""
    data = {}
    path = ROOT / "growth_score.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 6:
            continue
        ticker, total, quarterly_pts, nextyear_pts, fiveyear_pts, confidence = parts
        data[ticker] = {
            "growthscore": total, "growthscore_confidence": confidence,
            "growthscore_quarterly_pts": quarterly_pts,
            "growthscore_nextyear_pts": nextyear_pts,
            "growthscore_fiveyear_pts": fiveyear_pts,
        }
    return data


def load_overall_score():
    """ticker -> dict of total/confidence"""
    data = {}
    path = ROOT / "overall_score.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 5:
            continue
        ticker, total, _score_component, _secscore_component, confidence = parts
        data[ticker] = {"overallscore": total, "overallscore_confidence": confidence}
    return data


def load_prices():
    """ticker -> price, from fundamentals_data.tsv's own fresh Yahoo close -
    more reliably current than analyst_targets_*.txt's price field, which
    (see REFRESH_METHOD.md) no scan actually refreshes."""
    data = {}
    path = ROOT / "fundamentals_data.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 45:
            continue
        ticker, price = parts[0], parts[5]
        if price not in (None, "None", ""):
            data[ticker] = price
    return data


def load_existing_history():
    """date -> {ticker: line}, so today's rows can be replaced wholesale
    instead of appended blindly (idempotent re-runs)."""
    by_date = {}
    if not HISTORY_FILE.exists():
        return by_date
    for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != len(HISTORY_COLUMNS):
            continue
        date = parts[0]
        by_date.setdefault(date, {})[parts[1]] = line
    return by_date


def main():
    today = datetime.date.today().isoformat()
    scores = load_score()
    secondary_scores = load_secondary_score()
    risk_scores = load_risk_score()
    growth_scores = load_growth_score()
    overall_scores = load_overall_score()
    prices = load_prices()

    if not scores:
        print("No score.tsv found or it's empty - run compute_score.py first.")
        return

    all_tickers = (set(scores) | set(secondary_scores) | set(risk_scores)
                   | set(growth_scores) | set(overall_scores))

    by_date = load_existing_history()
    by_date[today] = {}  # replace today's rows entirely, not merge
    for ticker in all_tickers:
        row = {"date": today, "ticker": ticker, "price": prices.get(ticker, "")}
        row.update(scores.get(ticker, {}))
        row.update(secondary_scores.get(ticker, {}))
        row.update(risk_scores.get(ticker, {}))
        row.update(growth_scores.get(ticker, {}))
        row.update(overall_scores.get(ticker, {}))
        line = "\t".join(str(row.get(col, "")) for col in HISTORY_COLUMNS)
        by_date[today][ticker] = line

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        for date in sorted(by_date):
            for ticker in sorted(by_date[date]):
                f.write(by_date[date][ticker] + "\n")

    total_days = len(by_date)
    print(f"Score history: wrote {len(all_tickers)} rows for {today} "
          f"({total_days} distinct day(s) of history so far in {HISTORY_FILE.name})")


if __name__ == "__main__":
    main()
