"""
BACKTEST WEEKLY MOMENTUM - historical sanity check for the Weekly Momentum
Score, per the research's explicit warning: never trust a short-horizon
signal with real money before validating it out-of-sample, and always
compare tuned weights against an equal-weight benchmark (if tuning doesn't
clearly beat equal weights, the tuning is probably fit to noise).

Method (deliberately simple for a v1 - see WEEKLY_MOMENTUM_STATE.json):
  1. Fetch ~9 months of daily closes for a sample of the current liquid
     universe (reuses momentum_data.tsv's ticker list, but needs a longer
     history than that file stores, so this re-fetches with range=9mo).
  2. For each of several past "as-of" dates (spaced ~2 weeks apart, leaving
     at least 15 trading days of forward data after each), recompute the
     SAME z-scored components compute_weekly_momentum.py uses, purely from
     price/volume history available AS OF that date (no lookahead - this is
     the single most important discipline the research stresses).
  3. Take the top N ranked tickers as of that date, measure their actual
     forward return over the next HOLDING_DAYS trading days, applying the
     researched hard rules: exit early if price drops STOP_LOSS_PCT from
     entry (simulated stop), otherwise exit at the time-stop.
  4. Report win rate, average return, and a rough Sharpe estimate for the
     scored top-N picks, AND the same stats for a random-N control group
     drawn from the same universe/date - the real benchmark question is
     "does the score beat random", not "is the average return positive"
     (a rising market lifts everything).

This does NOT use the analyst-revision component (analyst_snapshot_history.tsv
has no historical depth to backtest against yet) - it only backtests the
price/volume-based components, which is still the majority of the weight.

Run: python backtest_weekly_momentum.py
Result: WEEKLY_MOMENTUM_BACKTEST.md
"""

import random
import statistics
import time
from pathlib import Path

import requests

from momentum_scan import compute_rsi, fetch_chart, load_universe

ROOT = Path(__file__).parent
REPORT_FILE = ROOT / "WEEKLY_MOMENTUM_BACKTEST.md"

SAMPLE_SIZE = 400          # subset of the liquid universe, to keep the fetch fast
NUM_AS_OF_DATES = 6        # spaced ~2 weeks apart, oldest first
DATE_SPACING_DAYS = 10     # trading days between as-of dates
HOLDING_DAYS = 10          # forward holding period (trading days)
STOP_LOSS_PCT = -8.0       # simulated hard stop, % from entry
TOP_N = 20
TURNOVER_CONFIRM_THRESHOLD = 1.2


def pct_return(closes, i_from, i_to):
    if i_from < 0 or i_to >= len(closes) or i_from >= i_to:
        return None
    old, new = closes[i_from], closes[i_to]
    if not old:
        return None
    return (new - old) / old * 100


def fetch_9mo(symbol):
    try:
        resp = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
            params={"range": "9mo", "interval": "1d"},
            headers={"User-Agent": "Mozilla/5.0 (eToroStockTracker research contact@example.com)"},
            timeout=15,
        )
    except requests.RequestException:
        return None, None
    if resp.status_code != 200:
        return None, None
    result = resp.json().get("chart", {}).get("result")
    if not result:
        return None, None
    quote = result[0]["indicators"]["quote"][0]
    raw_closes = quote.get("close") or []
    raw_volumes = quote.get("volume") or []
    closes, volumes = [], []
    for c, v in zip(raw_closes, raw_volumes):
        if c is not None and v is not None:
            closes.append(c)
            volumes.append(v)
    return closes, volumes


def zscore(values_by_ticker):
    clean = {t: v for t, v in values_by_ticker.items() if v is not None}
    if len(clean) < 10:
        return {}
    vals = list(clean.values())
    mean, stdev = statistics.mean(vals), statistics.pstdev(vals)
    if stdev == 0:
        return {t: 0.0 for t in clean}
    lo, hi = mean - 3 * stdev, mean + 3 * stdev
    return {t: (max(lo, min(hi, v)) - mean) / stdev for t, v in clean.items()}


def score_as_of(histories, as_of_idx):
    """histories: {ticker: (closes, volumes)}. as_of_idx: the index into each
    ticker's OWN closes/volumes array representing 'today' for this
    backtest point - only data at or before this index is used, so there is
    no lookahead."""
    momentum_turnover_raw, persist_raw, rsi2_raw = {}, {}, {}
    for t, (closes, volumes) in histories.items():
        if as_of_idx < 65 or as_of_idx >= len(closes):
            continue
        window_closes = closes[: as_of_idx + 1]
        window_volumes = volumes[: as_of_idx + 1]
        ret21 = pct_return(window_closes, len(window_closes) - 22, len(window_closes) - 1)
        vol5 = sum(window_volumes[-5:]) / 5
        vol30 = sum(window_volumes[-30:]) / 30
        vol60 = sum(window_volumes[-60:]) / 60
        turnover_ratio = window_volumes[-1] / vol30 if vol30 else None
        if ret21 is not None and turnover_ratio is not None:
            momentum_turnover_raw[t] = ret21 if turnover_ratio >= TURNOVER_CONFIRM_THRESHOLD else 0.0
        if vol60:
            persist_raw[t] = vol5 / vol60
        rsi2 = compute_rsi(window_closes, 2)
        if rsi2 is not None:
            rsi2_raw[t] = 100 - rsi2  # inverted, same convention as compute_weekly_momentum.py

    z_mom, z_persist, z_rsi2 = zscore(momentum_turnover_raw), zscore(persist_raw), zscore(rsi2_raw)
    weights = {"mom": 0.40, "persist": 0.30, "rsi2": 0.30}  # renormalized subset (no 52w/relstrength/revision in backtest v1)

    scores = {}
    for t in histories:
        parts = {}
        if t in z_mom:
            parts["mom"] = z_mom[t]
        if t in z_persist:
            parts["persist"] = z_persist[t]
        if t in z_rsi2:
            parts["rsi2"] = z_rsi2[t]
        if len(parts) < 2:
            continue
        wsum = sum(weights[k] for k in parts)
        scores[t] = sum(weights[k] * v for k, v in parts.items()) / wsum
    return scores


def simulate_forward(closes, entry_idx, holding_days, stop_loss_pct):
    entry_price = closes[entry_idx]
    if not entry_price:
        return None
    exit_idx = min(entry_idx + holding_days, len(closes) - 1)
    for i in range(entry_idx + 1, exit_idx + 1):
        change = (closes[i] - entry_price) / entry_price * 100
        if change <= stop_loss_pct:
            return change  # stopped out early
    final_idx = min(entry_idx + holding_days, len(closes) - 1)
    return (closes[final_idx] - entry_price) / entry_price * 100


def summarize(returns):
    if not returns:
        return {"n": 0, "win_rate": None, "avg_return": None, "sharpe_est": None}
    n = len(returns)
    win_rate = sum(1 for r in returns if r > 0) / n * 100
    avg = statistics.mean(returns)
    stdev = statistics.pstdev(returns) if n > 1 else 0
    sharpe_est = (avg / stdev) if stdev else None
    return {"n": n, "win_rate": win_rate, "avg_return": avg, "sharpe_est": sharpe_est}


def main():
    started = time.time()
    universe = load_universe()
    if len(universe) > SAMPLE_SIZE:
        random.seed(42)  # reproducible sample across runs
        universe = random.sample(universe, SAMPLE_SIZE)
    print(f"Backtest sample: {len(universe)} tickers, fetching 9mo history each...")

    histories = {}
    for i, t in enumerate(universe, 1):
        closes, volumes = fetch_9mo(t)
        if closes and len(closes) >= 100:
            histories[t] = (closes, volumes)
        if i % 50 == 0:
            print(f"  fetched {i}/{len(universe)}...")

    print(f"Got usable history for {len(histories)} tickers.")
    if len(histories) < 30:
        print("Not enough usable history to backtest meaningfully.")
        return

    min_len = min(len(c) for c, _ in histories.values())
    # As-of indices spaced DATE_SPACING_DAYS apart, leaving HOLDING_DAYS of
    # forward room after the LAST one and 65 days of trailing room before
    # the FIRST one (for the 60-day volume average).
    latest_possible = min_len - 1 - HOLDING_DAYS
    as_of_indices = [
        latest_possible - i * DATE_SPACING_DAYS
        for i in range(NUM_AS_OF_DATES)
        if latest_possible - i * DATE_SPACING_DAYS >= 65
    ]
    as_of_indices.reverse()  # oldest first
    print(f"Backtesting at {len(as_of_indices)} as-of points...")

    scored_returns, random_returns = [], []
    per_date_rows = []
    for as_of_idx in as_of_indices:
        scores = score_as_of(histories, as_of_idx)
        if len(scores) < TOP_N:
            continue
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        top_tickers = [t for t, _ in ranked[:TOP_N]]
        pool = [t for t in histories if t not in scores or True]  # full pool for random control
        random.seed(as_of_idx)
        random_tickers = random.sample(list(histories.keys()), TOP_N)

        top_rets = [simulate_forward(histories[t][0], as_of_idx, HOLDING_DAYS, STOP_LOSS_PCT) for t in top_tickers]
        top_rets = [r for r in top_rets if r is not None]
        rand_rets = [simulate_forward(histories[t][0], as_of_idx, HOLDING_DAYS, STOP_LOSS_PCT) for t in random_tickers]
        rand_rets = [r for r in rand_rets if r is not None]

        scored_returns.extend(top_rets)
        random_returns.extend(rand_rets)
        per_date_rows.append((as_of_idx, summarize(top_rets), summarize(rand_rets)))

    scored_summary = summarize(scored_returns)
    random_summary = summarize(random_returns)

    lines = ["# Weekly Momentum Score - Backtest Report\n\n"]
    lines.append(
        f"Sample: {len(universe)} tickers from the current liquid universe, {len(histories)} with usable "
        f"9-month history. {len(as_of_indices)} as-of points, {HOLDING_DAYS}-trading-day holding period, "
        f"{STOP_LOSS_PCT:.0f}% hard stop, top {TOP_N} ranked vs {TOP_N} random tickers as the control group.\n\n"
    )
    lines.append(
        "**This backtest uses only the price/volume components (momentum-with-turnover, volume persistence, "
        "RSI(2)) - the 52-week-position, relative-strength-vs-SPY, and analyst-revision components are not "
        "included here** (the first two need per-date historical fundamentals data this project doesn't "
        "retroactively have; the third has no historical depth yet). Treat this as a partial validation of "
        "the price/volume half of the score, not the full production formula.\n\n"
    )
    lines.append("## Overall: scored top-N vs random-N\n\n")
    lines.append("| Group | N trades | Win rate | Avg return | Sharpe (rough) |\n|---|---|---|---|---|\n")
    for label, s in (("Scored top-N", scored_summary), ("Random control", random_summary)):
        wr = f"{s['win_rate']:.1f}%" if s['win_rate'] is not None else "-"
        avg = f"{s['avg_return']:+.2f}%" if s['avg_return'] is not None else "-"
        sh = f"{s['sharpe_est']:.2f}" if s['sharpe_est'] is not None else "-"
        lines.append(f"| {label} | {s['n']} | {wr} | {avg} | {sh} |\n")
    lines.append("\n")

    edge = None
    if scored_summary["avg_return"] is not None and random_summary["avg_return"] is not None:
        edge = scored_summary["avg_return"] - random_summary["avg_return"]
        lines.append(
            f"**Edge over random: {edge:+.2f} percentage points per {HOLDING_DAYS}-trading-day trade.** "
            + (
                "This is a positive sign but a single backtest run is not proof of a real edge - "
                "paper-trade forward before risking real money, per the research's explicit guidance.\n\n"
                if edge > 0 else
                "This run shows NO edge over random selection - do not trust this score with real money "
                "until a re-run (more as-of dates, a different sample) shows a consistent positive edge.\n\n"
            )
        )

    lines.append("## Per as-of-date detail\n\n")
    lines.append("| As-of index | Scored N | Scored win% | Scored avg | Random N | Random win% | Random avg |\n|---|---|---|---|---|---|---|\n")
    for idx, top_s, rand_s in per_date_rows:
        lines.append(
            f"| {idx} | {top_s['n']} | {top_s['win_rate']:.0f}% | {top_s['avg_return']:+.2f}% | "
            f"{rand_s['n']} | {rand_s['win_rate']:.0f}% | {rand_s['avg_return']:+.2f}% |\n"
        )

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

    elapsed = time.time() - started
    print(f"Backtest done in {elapsed/60:.1f} min -> {REPORT_FILE.name}")
    if edge is not None:
        print(f"Edge over random: {edge:+.2f} pp per trade")


if __name__ == "__main__":
    main()
