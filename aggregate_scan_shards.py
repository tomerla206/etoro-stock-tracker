"""
Combines the per-shard JSON outputs from the parallel cloud pipeline
(megascan.py / megascan_yahoo.py / fundamentals_scan.py, each run several
times in parallel with SHARD_INDEX/SHARD_COUNT set) into the real shared data
files, then runs the same downstream chain each of those scripts used to run
solo at the end of its own main() - exactly once, here, instead of once per
shard (which would have raced on every shared file and rebuilt the site N
times over for nothing).

insider_scan.py is NOT sharded (already fast via plain HTTP) and needs no
aggregation - it wrote its own final files directly in its own parallel job.

Run: python aggregate_scan_shards.py  (from the "aggregate" job, after
downloading every shard's shard_out/*.json artifact into ./shard_out/)
"""

import glob
import json
import subprocess
import sys
from pathlib import Path

import megascan
import megascan_yahoo
import fundamentals_scan

ROOT = Path(__file__).parent


def aggregate_megascan():
    files = sorted(glob.glob(str(ROOT / "shard_out" / "megascan_shard*.json")))
    if not files:
        print("No megascan shards found - skipping.")
        return
    changed, consensus, hedgefund = [], {}, {}
    new_green = lost_coverage = refreshed = unchanged = 0
    errors = []
    for fp in files:
        d = json.loads(Path(fp).read_text(encoding="utf-8"))
        changed.extend(d["changed"])
        consensus.update(d["consensus"])
        hedgefund.update(d["hedgefund"])
        new_green += len(d["new_green"])
        lost_coverage += len(d["lost_coverage"])
        refreshed += len(d["refreshed"])
        unchanged += len(d["unchanged"])
        errors.extend(d["errors"])

    print(f"Applying changes from {len(files)} MEGASCAN shards ({len(changed)} rows changed)...")
    megascan.apply_changes(changed)

    with open(ROOT / "consensus_ratings.txt", "w", encoding="utf-8") as f:
        for ticker, (pct, rating) in consensus.items():
            f.write(f"{ticker}\t{pct}\t{rating}\n")

    with open(ROOT / "hedge_fund_activity.tsv", "w", encoding="utf-8") as f:
        for ticker, (added, reduced, unch, total) in hedgefund.items():
            f.write(f"{ticker}\t{added}\t{reduced}\t{unch}\t{total}\n")

    with open(ROOT / "MEGASCAN_RESULTS.md", "w", encoding="utf-8") as f:
        f.write("# MEGASCAN Results (aggregated from shards)\n\n")
        f.write(f"New GREEN (yellow -> green): {new_green}\n")
        f.write(f"Lost coverage (green -> yellow): {lost_coverage}\n")
        f.write(f"Refreshed, still green: {refreshed}\n")
        f.write(f"Still yellow, unchanged: {unchanged}\n")
        f.write(f"Errors ({len(errors)}): " + ", ".join(errors) + "\n")

    print("MEGASCAN aggregation complete.")


def aggregate_megascan_yahoo():
    files = sorted(glob.glob(str(ROOT / "shard_out" / "megascan_yahoo_shard*.json")))
    if not files:
        print("No megascan_yahoo shards found - skipping.")
        return
    new_targets, new_dividends = {}, {}
    updated, no_data, errors = [], [], []
    for fp in files:
        d = json.loads(Path(fp).read_text(encoding="utf-8"))
        for ticker, (target, currency) in d["targets"].items():
            new_targets[ticker] = (target, currency)
        new_dividends.update(d["dividends"])
        updated.extend(d["updated"])
        no_data.extend(d["no_data"])
        errors.extend(d["errors"])

    # Every shard only scanned tickers still missing from the checkpoint (see
    # megascan_yahoo.py's own already_done filter), so merging its new
    # entries on top of the checkpoint - not replacing it - preserves
    # everything scanned on previous days/runs.
    prev_targets, prev_dividends = megascan_yahoo.load_checkpoint()
    merged_targets = dict(prev_targets)
    merged_targets.update(new_targets)
    merged_dividends = dict(prev_dividends)
    merged_dividends.update(new_dividends)

    print(f"Merging {len(files)} MEGASCAN YAHOO shards ({len(new_targets)} new targets, "
          f"{len(new_dividends)} new dividends) into the checkpoint...")
    with open(ROOT / "yahoo_targets_0_MEGASCAN.txt", "w", encoding="utf-8") as f:
        for ticker, (target, currency) in merged_targets.items():
            avg = f"{target:.4f}" if target is not None else ""
            f.write(f"{ticker}\t\t{avg}\t\t{currency}\n")
    with open(ROOT / "yahoo_dividends_MEGASCAN.txt", "w", encoding="utf-8") as f:
        for ticker, div in merged_dividends.items():
            f.write(f"{ticker}\t{div}\n")

    all_tickers = megascan_yahoo.load_all_tickers()
    still_missing = [t for t in all_tickers if t not in merged_targets and t not in merged_dividends]
    with open(ROOT / "MEGASCAN_YAHOO_RESULTS.md", "w", encoding="utf-8") as f:
        f.write("# MEGASCAN YAHOO Results (aggregated from shards)\n\n")
        f.write(f"Full universe: {len(all_tickers)} | Updated this run: {len(updated)} | "
                f"No data: {len(no_data)} | Errors: {len(errors)} | "
                f"Still missing any data: {len(still_missing)}\n\n")
        f.write(f"## Errors this run ({len(errors)})\n")
        f.write(", ".join(errors) + "\n")

    print("MEGASCAN YAHOO aggregation complete.")


def aggregate_fundamentals():
    files = sorted(glob.glob(str(ROOT / "shard_out" / "fundamentals_shard*.json")))
    if not files:
        print("No fundamentals shards found - skipping.")
        return
    data = {}
    updated, no_data, errors = [], [], []
    for fp in files:
        d = json.loads(Path(fp).read_text(encoding="utf-8"))
        data.update(d["data"])
        updated.extend(d["updated"])
        no_data.extend(d["no_data"])
        errors.extend(d["errors"])

    print(f"Merging {len(files)} FUNDAMENTALS SCAN shards ({len(data)} tickers with data)...")
    results = {"data": data, "updated": updated, "no_data": no_data, "errors": errors}
    fundamentals_scan.write_data_file(results)
    fundamentals_scan.write_sector_file(results)

    with open(ROOT / "FUNDAMENTALS_SCAN_RESULTS.md", "w", encoding="utf-8") as f:
        f.write("# FUNDAMENTALS SCAN Results (aggregated from shards)\n\n")
        f.write(f"Updated: {len(updated)} | No data: {len(no_data)} | Errors: {len(errors)}\n")

    print("FUNDAMENTALS SCAN aggregation complete.")


def main():
    aggregate_megascan()
    aggregate_megascan_yahoo()
    aggregate_fundamentals()

    # Same downstream chain fundamentals_scan.py's own main() used to run
    # solo at the end - centralized here so it runs exactly once, on the
    # fully-merged data, instead of once per shard.
    print("Refreshing Price and computing Score (raw data files only)...")
    for script in (
        "update_price.py", "compute_score.py", "compute_secondary_score.py",
        "compute_risk_score.py", "compute_growth_score.py", "compute_overall_score.py",
        "compute_score_percentile.py",
    ):
        subprocess.run([sys.executable, script], cwd=ROOT, check=False)

    print("Appending today's snapshot to score_history.tsv...")
    subprocess.run([sys.executable, "score_history.py"], cwd=ROOT, check=False)

    print("Updating signal backtest (no-ops quietly until enough daily history accumulates)...")
    subprocess.run([sys.executable, "backtest_signals.py"], cwd=ROOT, check=False)

    print("Checking for meaningful day-over-day Score changes...")
    subprocess.run([sys.executable, "compute_score_change.py"], cwd=ROOT, check=False)

    print("Rebuilding site (build_site.py runs every merge script + reassembles)...")
    subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=False)

    print("Aggregation complete.")


if __name__ == "__main__":
    main()
