"""
CHECK RE-ENTRY OPPORTUNITIES - watches every position in exit_history.tsv
(tickers sold for a realized profit - see parse_exit_history.py) for a
good moment to buy back in: the price has pulled back some from where you
sold, but the analyst target still implies real upside from today's price.

Built for a specific, repeated pattern: sell a winner to lock in a gain
instead of riding it back down (avoiding pure speculation), then watch
from the sidelines in case it dips further but the long-term case is
still intact - rather than either chasing it back up immediately or
forgetting about it entirely.

Alert logic (both conditions required):
  1. Price has dropped at least PULLBACK_THRESHOLD_PCT since your exit
     price - a real pullback, not just noise around the price you sold at.
  2. The analyst average target still implies at least
     UPSIDE_THRESHOLD_PCT upside from TODAY'S price - the original
     long-term case (whatever made you buy it in the first place) is
     still intact, not something that already played out or reversed.

Uses fundamentals_data.tsv for today's price (refreshed daily by
FUNDAMENTALS SCAN - the same source score_history.py itself uses) and
analyst_targets_*.txt for the average analyst target - no new data
source needed, both already exist from the daily scan pipeline.

This is a heuristic screening aid, not investment advice - a stock
meeting both conditions isn't guaranteed to be a good buy, it's just
worth a second look you might otherwise not have taken.

exit_history.tsv and REENTRY_WATCHLIST.md are both gitignored (same
sensitivity as portfolio_real.tsv - they reveal real trading activity) -
this only ever runs in fundamentals_scan.py's LOCAL daily chain, never in
aggregate_scan_shards.py's cloud-parallel chain, since the cloud runner's
checkout never has (and never should have) exit_history.tsv to read.

Run: python check_reentry_opportunities.py (after fundamentals_scan.py
has produced a fresh fundamentals_data.tsv)
Result: REENTRY_WATCHLIST.md
"""

import glob
from pathlib import Path

ROOT = Path(__file__).parent
EXIT_HISTORY_FILE = ROOT / "exit_history.tsv"
RESULTS_FILE = ROOT / "REENTRY_WATCHLIST.md"

PULLBACK_THRESHOLD_PCT = 5.0
UPSIDE_THRESHOLD_PCT = 20.0


def f(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def load_exit_history():
    """ticker -> list of {exit_date, exit_price, pl_pct, account} - a
    ticker can appear more than once (sold, re-bought, sold again on a
    different account or a different day)."""
    data = {}
    if not EXIT_HISTORY_FILE.exists():
        return data
    for line in EXIT_HISTORY_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 5:
            continue
        ticker, exit_date, exit_price, pl_pct, account = parts
        exit_price = f(exit_price)
        if exit_price is None:
            continue
        data.setdefault(ticker, []).append({
            "exit_date": exit_date, "exit_price": exit_price,
            "pl_pct": f(pl_pct), "account": account,
        })
    return data


def load_current_prices():
    """ticker -> current price, from fundamentals_data.tsv (same source
    score_history.py uses - refreshed daily by FUNDAMENTALS SCAN)."""
    data = {}
    path = ROOT / "fundamentals_data.tsv"
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 45:
            continue
        price = f(parts[5])
        if price is not None and price > 0:
            data[parts[0]] = price
    return data


def load_analyst_targets():
    """ticker -> average analyst target price, from analyst_targets_*.txt."""
    data = {}
    files = sorted(fn for fn in glob.glob(str(ROOT / "analyst_targets_*.txt")) if "_OLD" not in fn)
    for fname in files:
        for line in Path(fname).read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != 8:
                continue
            ticker, _name, _price, _low, avg, _high, status, _trade = parts
            if status not in ("OK", "CVR"):
                continue
            avg = f(avg)
            if avg:
                data[ticker] = avg
    return data


def main():
    exits = load_exit_history()
    if not exits:
        msg = ("No exit_history.tsv yet (or it's empty) - nothing to check. Build it with "
               "parse_exit_history.py from eToro's own /portfolio/history page (a live-session "
               "step, see REFRESH_METHOD.md's SCAN EXIT HISTORY section) whenever you realize a "
               "profitable exit worth watching for a re-entry.")
        print(msg)
        with open(RESULTS_FILE, "w", encoding="utf-8") as out:
            out.write("# Re-entry Watchlist\n\n" + msg + "\n")
        return

    prices = load_current_prices()
    targets = load_analyst_targets()

    candidates = []
    for ticker, records in exits.items():
        current_price = prices.get(ticker)
        target = targets.get(ticker)
        if current_price is None or target is None:
            continue
        # Use the most recent exit for this ticker as "the" exit to compare
        # against - a later sale supersedes an earlier one as the relevant
        # reference point.
        latest_exit = max(records, key=lambda r: r["exit_date"])
        exit_price = latest_exit["exit_price"]

        pullback_pct = (exit_price - current_price) / exit_price * 100
        upside_pct = (target - current_price) / current_price * 100

        if pullback_pct >= PULLBACK_THRESHOLD_PCT and upside_pct >= UPSIDE_THRESHOLD_PCT:
            candidates.append({
                "ticker": ticker, "exit_date": latest_exit["exit_date"],
                "exit_price": exit_price, "current_price": current_price,
                "target": target, "pullback_pct": pullback_pct,
                "upside_pct": upside_pct, "account": latest_exit["account"],
            })

    candidates.sort(key=lambda c: c["upside_pct"], reverse=True)

    lines = [
        "# Re-entry Watchlist\n\n",
        f"Tracking {len(exits)} previously-exited ticker(s). A candidate needs BOTH: price down "
        f"at least {PULLBACK_THRESHOLD_PCT:.0f}% from your exit price, AND analyst average target "
        f"still at least {UPSIDE_THRESHOLD_PCT:.0f}% above today's price.\n\n",
        f"**{len(candidates)} candidate(s) today**\n\n",
    ]
    if candidates:
        lines.append("| Ticker | Exit date | Exit $ | Now $ | Down since exit | Target $ | Upside to target | Account |\n")
        lines.append("|---|---|---|---|---|---|---|---|\n")
        for c in candidates:
            lines.append(
                f"| {c['ticker']} | {c['exit_date']} | {c['exit_price']:.2f} | "
                f"{c['current_price']:.2f} | {c['pullback_pct']:+.1f}% | {c['target']:.2f} | "
                f"{c['upside_pct']:+.1f}% | {c['account']} |\n"
            )

    with open(RESULTS_FILE, "w", encoding="utf-8") as out:
        out.writelines(lines)

    print(f"Checked {len(exits)} exited tickers, {len(candidates)} re-entry candidate(s) -> {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
