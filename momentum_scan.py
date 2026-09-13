"""
MOMENTUM SCAN - short-term (1 week to 1 month) price/volume signals feeding
the Weekly Momentum Score (a separate, deliberately SPECULATIVE screen, not
part of the main long-horizon Score - see WEEKLY_MOMENTUM_STATE.json for the
research this is based on).

Pure HTTP (requests + ThreadPoolExecutor), same class of method as
fundamentals_scan.py, but INTENTIONALLY DECOUPLED from it: its own fetch
loop, its own output file, its own (much smaller) universe. This is not an
oversight - two reasons:
  1. Short-term signals only make sense on LIQUID US tickers (see research:
     the turnover-momentum interaction effect is specifically about heavily-
     traded names). Restricting the universe up front to no-dot-suffix
     (US NASDAQ/NYSE, matching this project's existing ticker convention)
     tickers with price >= MIN_PRICE cuts ~6,761 down to a few thousand
     BEFORE any network call, not after.
  2. Keeping this fetch loop separate means a bug or rate-limit issue here
     can never break the main fundamentals_scan.py pipeline that everything
     else (Score, Secondary Score, Risk Score) depends on.

Only the Yahoo `chart` endpoint is needed (daily OHLCV, no crumb/cookie
handshake required - that's only for quoteSummary, which this script never
calls), fetched with range=6mo (enough history for the 60-day trailing
volume average and 21-day return; NOT enough for a fresh 52-week-high calc,
which is deliberately not recomputed here - it's joined in from
fundamentals_data.tsv's already-computed range52_pos field instead, see
compute_weekly_momentum.py).

Run: python momentum_scan.py
Result: momentum_data.tsv
  (TICKER, price, ret5d, ret10d, ret21d, volAvg5d, volAvg30d, volAvg60d,
   turnoverRatio, turnoverPersist, rsi2, relStrength10d)
  ret*d are percent returns. turnoverRatio = today's volume / 30-day average
  (the "is this heavily traded right now" half of the turnover-momentum
  interaction). turnoverPersist = 5-day avg volume / 60-day avg volume (is
  elevated volume a one-day blip or a sustained shift). relStrength10d is
  this ticker's 10-day return minus SPY's own 10-day return over the same
  window (percentage points).
"""

import concurrent.futures
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent
HEADERS = {"User-Agent": "Mozilla/5.0 (eToroStockTracker research contact@example.com)"}
WORKERS = 8
LOG_EVERY = 100
MIN_PRICE = 5.0
FUNDAMENTALS_FILE = ROOT / "fundamentals_data.tsv"
OUTPUT_FILE = ROOT / "momentum_data.tsv"
LOG_FILE = ROOT / "MOMENTUM_SCAN_LOG.md"


def load_universe():
    """Liquid US tickers only: no '.' in the ticker (this project's existing
    convention for a bare NASDAQ/NYSE symbol - every foreign exchange listing
    carries a suffix like .L/.DE/.ASX) AND price >= MIN_PRICE, both read from
    fundamentals_data.tsv (already-scanned, no extra network cost for this
    filtering step)."""
    tickers = []
    if not FUNDAMENTALS_FILE.exists():
        return tickers
    for line in FUNDAMENTALS_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 45:
            continue
        ticker = parts[0]
        if "." in ticker:
            continue
        try:
            price = float(parts[5])
        except (ValueError, TypeError):
            continue
        if price >= MIN_PRICE:
            tickers.append(ticker)
    return tickers


def compute_rsi(closes, period):
    """Wilder-smoothed RSI for an arbitrary period (period=2 for the
    Connors-style fast oscillator, period=14 for the standard one), from a
    list of daily closes oldest-first. Returns None if there isn't enough
    history."""
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def pct_return(closes, days_back):
    if len(closes) <= days_back:
        return None
    old, new = closes[-1 - days_back], closes[-1]
    if not old:
        return None
    return (new - old) / old * 100


def fetch_chart(symbol):
    """Returns (closes, volumes) oldest-first, or (None, None) on failure."""
    try:
        resp = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
            params={"range": "6mo", "interval": "1d"}, headers=HEADERS, timeout=15,
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


def compute_signals(closes, volumes):
    if len(closes) < 22 or len(volumes) < 22:
        return None
    price = closes[-1]
    ret5d = pct_return(closes, 5)
    ret10d = pct_return(closes, 10)
    ret21d = pct_return(closes, 21)
    vol5 = sum(volumes[-5:]) / 5
    vol30 = sum(volumes[-30:]) / 30 if len(volumes) >= 30 else None
    vol60 = sum(volumes[-60:]) / 60 if len(volumes) >= 60 else None
    turnover_ratio = (volumes[-1] / vol30) if vol30 else None
    turnover_persist = (vol5 / vol60) if vol60 else None
    rsi2 = compute_rsi(closes, 2)
    return {
        "price": price, "ret5d": ret5d, "ret10d": ret10d, "ret21d": ret21d,
        "vol5": vol5, "vol30": vol30, "vol60": vol60,
        "turnover_ratio": turnover_ratio, "turnover_persist": turnover_persist,
        "rsi2": rsi2,
    }


def scan_one(ticker):
    closes, volumes = fetch_chart(ticker)
    if not closes:
        return ticker, None
    sig = compute_signals(closes, volumes)
    return ticker, sig


def main():
    started = time.time()
    universe = load_universe()
    if not universe:
        print("No universe tickers found (fundamentals_data.tsv missing or empty) - nothing to scan.")
        return

    print(f"Fetching SPY's own 10-day return as the relative-strength benchmark...")
    spy_closes, _ = fetch_chart("SPY")
    spy_ret10d = pct_return(spy_closes, 10) if spy_closes else None
    if spy_ret10d is None:
        print("WARNING: could not fetch SPY - relative strength will be blank for every ticker this run.")

    print(f"Scanning {len(universe)} liquid US tickers (price >= ${MIN_PRICE:.0f})...")
    results = {}
    no_data = []
    done = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = {ex.submit(scan_one, t): t for t in universe}
        for future in concurrent.futures.as_completed(futures):
            ticker, sig = future.result()
            done += 1
            if sig is None:
                no_data.append(ticker)
            else:
                results[ticker] = sig
            if done % LOG_EVERY == 0 or done == len(universe):
                elapsed = time.time() - started
                rate = done / elapsed if elapsed > 0 else 0
                remaining = (len(universe) - done) / rate if rate > 0 else 0
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    f.write("# MOMENTUM SCAN progress\n\n")
                    f.write(f"Done: {done} / {len(universe)}\n\n")
                    f.write(f"Elapsed: {elapsed/60:.1f} min | Rate: {rate:.2f}/s | ETA: {remaining/60:.1f} min\n\n")
                    f.write(f"Updated: {len(results)}\n")
                    f.write(f"No data: {len(no_data)}\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for ticker, sig in results.items():
            rel_strength_10d = (
                (sig["ret10d"] - spy_ret10d) if sig["ret10d"] is not None and spy_ret10d is not None else None
            )
            f.write(
                f"{ticker}\t{sig['price']}\t{sig['ret5d']}\t{sig['ret10d']}\t{sig['ret21d']}\t"
                f"{sig['vol5']}\t{sig['vol30']}\t{sig['vol60']}\t"
                f"{sig['turnover_ratio']}\t{sig['turnover_persist']}\t{sig['rsi2']}\t{rel_strength_10d}\n"
            )

    elapsed = time.time() - started
    print(f"Momentum scan done in {elapsed/60:.1f} min: {len(results)} updated, {len(no_data)} no-data -> {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
