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


def load_held_tickers(account):
    """Set of tickers currently held (or pending) in portfolio_<account>.tsv -
    no header row, ticker is always column 0. A ticker already back in the
    portfolio is not a re-entry candidate anymore; showing it as one (as
    happened with TNYA - sold part of a position for profit, still holding
    the rest) is just noise pointing at a position you're already in."""
    path = ROOT / f"portfolio_{account}.tsv"
    if not path.exists():
        return set()
    held = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if parts and parts[0]:
            held.add(parts[0])
    return held


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
    held = {"real": load_held_tickers("real"), "virtual": load_held_tickers("virtual")}

    candidates = []
    skipped_held = 0
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

        # Already back in that same account (e.g. sold part of a position
        # for profit, still holding the rest) - not a re-entry opportunity
        # anymore, you're already in it. A different account re-entering
        # what THIS account exited is still worth flagging, so the check is
        # per-account, not "held anywhere".
        if ticker in held.get(latest_exit["account"], ()):
            skipped_held += 1
            continue

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
        f"still at least {UPSIDE_THRESHOLD_PCT:.0f}% above today's price. Tickers already held "
        f"again in the same account are excluded (that's not a re-entry, it's already happened) "
        f"- {skipped_held} skipped for that reason this run.\n\n",
        f"**{len(candidates)} candidate(s) today**\n\n",
    ]
    # Split into two separate tables, Real then Virtual - keeping the two
    # accounts' candidates visually apart instead of interleaved in one
    # mixed table sorted purely by upside (which was confusing: seeing
    # "TNYA (virtual)" and a Real-account candidate back to back reads as
    # one combined list when they're really two separate portfolios).
    for account_label, account_key in (("Real", "real"), ("Virtual", "virtual")):
        account_candidates = [c for c in candidates if c["account"] == account_key]
        lines.append(f"## {account_label} ({len(account_candidates)})\n\n")
        if not account_candidates:
            lines.append("_No candidates._\n\n")
            continue
        lines.append("| Ticker | Exit date | Exit $ | Now $ | Down since exit | Target $ | Upside to target |\n")
        lines.append("|---|---|---|---|---|---|---|\n")
        for c in account_candidates:
            lines.append(
                f"| {c['ticker']} | {c['exit_date']} | {c['exit_price']:.2f} | "
                f"{c['current_price']:.2f} | {c['pullback_pct']:+.1f}% | {c['target']:.2f} | "
                f"{c['upside_pct']:+.1f}% |\n"
            )
        lines.append("\n")

    with open(RESULTS_FILE, "w", encoding="utf-8") as out:
        out.writelines(lines)

    print(f"Checked {len(exits)} exited tickers ({skipped_held} already held again, skipped), "
          f"{len(candidates)} re-entry candidate(s) -> {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
