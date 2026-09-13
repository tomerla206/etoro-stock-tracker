"""
COMPUTE WEEKLY MOMENTUM SCORE - combines momentum_data.tsv (Stage 1),
fundamentals_data.tsv's already-computed range52_pos (52-week-range
position, reused not recomputed), and analyst_snapshot_history.tsv's
revision delta (Stage 2) into one ranked, speculative short-term score.

SPECULATIVE AND SEPARATE from the main long-horizon Score by design - see
WEEKLY_MOMENTUM_STATE.json for the research this weighting is based on.
Do not blend this into compute_score.py/merge_score.py; it lives entirely
in its own pipeline and its own page (weekly_momentum.html).

Method: winsorize each raw signal at +-3 standard deviations (clip outliers
without dropping the ticker), z-score it across the liquid universe (mean 0,
std 1, so different-scaled signals like "percent return" and "RSI value" can
be summed meaningfully), then a fixed weighted sum. Weights come directly
from the research summary:
  - 21d return, but ONLY counted if turnover_ratio > 1.2 (today's volume is
    at least 20% above its 30-day average) - this is the single most
    important nuance from the research (Medhat & Schmeling 2022): momentum
    without volume confirmation tends to REVERSE, not continue, at this
    horizon. Below that volume bar the signal is zeroed out rather than
    inverted (a deliberate simplification - full sign-flipping needs more
    validation than a first version warrants).                    weight 20%
  - 52-week-high proximity (range52_pos, 0-100)                    weight 15%
  - turnover persistence (5d avg volume / 60d avg volume)          weight 15%
  - relative strength vs SPY, 10-day                                weight 15%
  - RSI(2) - inverted (low RSI(2) = oversold = timing edge per the
    Connors research), used as a timing overlay not a standalone bet weight 10%
  - analyst revision % over the last ~2-3 weeks                    weight 15%
  - (10% reserved, unused until the Stage 8 earnings-proximity flag exists -
    the total of the 6 active weights is 90%, not 100%, on purpose)

Run: python compute_weekly_momentum.py (after momentum_scan.py and
analyst_snapshot.py have both produced fresh output)
Result: weekly_momentum_score.tsv, ranked descending by score
  (RANK, TICKER, SCORE, RET21D, TURNOVER_RATIO, RANGE52_POS,
   TURNOVER_PERSIST, REL_STRENGTH_10D, RSI2, ANALYST_REVISION_PCT)
"""

import statistics
from pathlib import Path

ROOT = Path(__file__).parent
MOMENTUM_FILE = ROOT / "momentum_data.tsv"
FUNDAMENTALS_FILE = ROOT / "fundamentals_data.tsv"
OUTPUT_FILE = ROOT / "weekly_momentum_score.tsv"

WEIGHTS = {
    "momentum_turnover": 0.20,
    "range52_pos": 0.15,
    "turnover_persist": 0.15,
    "rel_strength_10d": 0.15,
    "rsi2_timing": 0.10,
    "analyst_revision": 0.15,
}
TURNOVER_CONFIRM_THRESHOLD = 1.2  # today's volume must be >= 1.2x its 30d average
MIN_DOLLAR_VOLUME = 2_000_000  # price * 30d avg volume, filters out thin names
                                # whose turnover ratios are extreme noise, not
                                # a real signal (research recommends $5M; using
                                # a lighter $2M bar here to keep more coverage
                                # for a v1, worth revisiting after backtesting)


def f(v):
    try:
        fv = float(v)
        return fv if fv == fv else None  # filters out NaN
    except (ValueError, TypeError):
        return None


def load_momentum():
    data = {}
    if not MOMENTUM_FILE.exists():
        return data
    for line in MOMENTUM_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 12:
            continue
        ticker = parts[0]
        data[ticker] = {
            "price": f(parts[1]), "ret5d": f(parts[2]), "ret10d": f(parts[3]),
            "ret21d": f(parts[4]), "vol5": f(parts[5]), "vol30": f(parts[6]),
            "vol60": f(parts[7]), "turnover_ratio": f(parts[8]),
            "turnover_persist": f(parts[9]), "rsi2": f(parts[10]),
            "rel_strength_10d": f(parts[11]),
        }
    return data


def load_range52_pos():
    data = {}
    if not FUNDAMENTALS_FILE.exists():
        return data
    for line in FUNDAMENTALS_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 45:
            continue
        pos = f(parts[13])
        if pos is not None:
            data[parts[0]] = pos
    return data


def load_analyst_revision():
    try:
        from analyst_snapshot import compute_analyst_revision
        return compute_analyst_revision()
    except Exception:
        return {}


def winsorize_zscore(values_by_ticker):
    """values_by_ticker: {ticker: float or None}. Returns {ticker: zscore},
    omitting tickers whose raw value was None. Clips at +-3 std before
    z-scoring so a handful of extreme outliers (a 300% one-week spike on a
    thinly-traded name, say) don't dominate the whole ranking."""
    clean = {t: v for t, v in values_by_ticker.items() if v is not None}
    if len(clean) < 10:
        return {}
    vals = list(clean.values())
    mean = statistics.mean(vals)
    stdev = statistics.pstdev(vals)
    if stdev == 0:
        return {t: 0.0 for t in clean}
    lo, hi = mean - 3 * stdev, mean + 3 * stdev
    clipped = {t: max(lo, min(hi, v)) for t, v in clean.items()}
    return {t: (v - mean) / stdev for t, v in clipped.items()}


def main():
    momentum = load_momentum()
    range52 = load_range52_pos()
    revisions = load_analyst_revision()

    if not momentum:
        print("No momentum_data.tsv found - run momentum_scan.py first.")
        return

    tickers = [
        t for t, m in momentum.items()
        if m["price"] is not None and m["vol30"] is not None
        and m["price"] * m["vol30"] >= MIN_DOLLAR_VOLUME
    ]
    dropped_illiquid = len(momentum) - len(tickers)

    # Momentum-with-turnover-confirmation: 21d return, zeroed out (not
    # inverted) when turnover_ratio doesn't clear the confirmation bar.
    momentum_turnover_raw = {}
    for t in tickers:
        m = momentum[t]
        if m["ret21d"] is None or m["turnover_ratio"] is None:
            continue
        momentum_turnover_raw[t] = m["ret21d"] if m["turnover_ratio"] >= TURNOVER_CONFIRM_THRESHOLD else 0.0

    turnover_persist_raw = {t: momentum[t]["turnover_persist"] for t in tickers}
    rel_strength_raw = {t: momentum[t]["rel_strength_10d"] for t in tickers}
    # RSI(2) timing: LOWER is better (oversold pullback within an uptrend is
    # the Connors entry), so invert before z-scoring - a positive z-score
    # should always mean "more favorable for this component".
    rsi2_timing_raw = {t: (100 - momentum[t]["rsi2"]) if momentum[t]["rsi2"] is not None else None for t in tickers}
    range52_raw = {t: range52.get(t) for t in tickers}
    revision_raw = {t: revisions.get(t) for t in tickers}

    z_momentum = winsorize_zscore(momentum_turnover_raw)
    z_persist = winsorize_zscore(turnover_persist_raw)
    z_relstrength = winsorize_zscore(rel_strength_raw)
    z_rsi2 = winsorize_zscore(rsi2_timing_raw)
    z_range52 = winsorize_zscore(range52_raw)
    z_revision = winsorize_zscore(revision_raw)

    have_revision_data = len(z_revision) >= 10
    active_weights = dict(WEIGHTS)
    if not have_revision_data:
        # Not enough analyst_snapshot_history.tsv depth yet (needs ~2-3
        # weeks of daily runs) - redistribute its weight proportionally
        # across the other components rather than silently zeroing 15% of
        # the score for every ticker.
        del active_weights["analyst_revision"]
        total = sum(active_weights.values())
        active_weights = {k: v / total * sum(WEIGHTS.values()) for k, v in active_weights.items()}

    scores = []
    for t in tickers:
        components = {
            "momentum_turnover": z_momentum.get(t),
            "range52_pos": z_range52.get(t),
            "turnover_persist": z_persist.get(t),
            "rel_strength_10d": z_relstrength.get(t),
            "rsi2_timing": z_rsi2.get(t),
        }
        if have_revision_data:
            components["analyst_revision"] = z_revision.get(t)

        present = {k: v for k, v in components.items() if v is not None}
        if len(present) < 3:
            continue  # too much missing data for this ticker to trust a score
        weight_sum = sum(active_weights[k] for k in present)
        score = sum(active_weights[k] * v for k, v in present.items()) / weight_sum

        m = momentum[t]
        scores.append({
            "ticker": t, "score": score, "ret21d": m["ret21d"],
            "turnover_ratio": m["turnover_ratio"], "range52_pos": range52.get(t),
            "turnover_persist": m["turnover_persist"], "rel_strength_10d": m["rel_strength_10d"],
            "rsi2": m["rsi2"], "analyst_revision_pct": revisions.get(t),
        })

    scores.sort(key=lambda c: c["score"], reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for i, c in enumerate(scores, 1):
            f_out.write(
                f"{i}\t{c['ticker']}\t{c['score']:.4f}\t{c['ret21d']}\t{c['turnover_ratio']}\t"
                f"{c['range52_pos']}\t{c['turnover_persist']}\t{c['rel_strength_10d']}\t"
                f"{c['rsi2']}\t{c['analyst_revision_pct']}\n"
            )

    print(f"Ranked {len(scores)} tickers ({dropped_illiquid} dropped for thin liquidity) -> {OUTPUT_FILE.name} "
          f"(analyst revision data {'included' if have_revision_data else 'NOT YET available - weight redistributed'})")


if __name__ == "__main__":
    main()
