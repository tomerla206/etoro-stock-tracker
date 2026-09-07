"""
MEGASCAN — full-exchange TipRanks coverage sweep (all 6,761 tickers).

Unlike the earlier paced-Claude-agent refresh (which only ever covered the
~4,330 already-GREEN tickers, 15-20s/ticker, human-paced for eToro-block-risk
reasons that don't apply to TipRanks), this scans EVERY ticker across every
analyst_targets_*.txt file, using the same local headless-Chromium method as
portfolio_server.py (free, no LLM, no eToro login/rate-limit risk).

For each ticker it re-checks TipRanks coverage and updates Low/Avg/High +
AnalysisStatus (OK/NOFAQ) in place. TRADEABLE/NOT_TRADEABLE (red) is an
eToro-side fact this script cannot verify (TipRanks has no tradeability
info) — those columns are left untouched; only coverage (yellow<->green)
transitions are detected and logged.

Run: python megascan.py
Progress:  MEGASCAN_LOG.md (updated every 50 tickers)
Result:    MEGASCAN_RESULTS.md (written at the end)
"""

import asyncio
import glob
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
TIPRANKS_URL = "https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={}&theme=light"
SUFFIX_STRIP = (".US", ".A", ".B", ".EUR")
CONCURRENCY = 8
LOG_EVERY = 50


def strip_suffix(ticker):
    for suf in SUFFIX_STRIP:
        if ticker.endswith(suf):
            return ticker[: -len(suf)]
    if ticker.endswith("/V"):
        return ticker[:-2]
    return ticker


def parse_low_avg_high(text):
    m = re.search(
        r"([\d,]+\.?\d*)\s*(?:Low\s*)?LOW ESTIMATE.*?([\d,]+\.?\d*)\s*AVERAGE PRICE TARGET.*?([\d,]+\.?\d*)\s*HIGH ESTIMATE",
        text,
        re.S,
    )
    if m:
        return (
            float(m.group(1).replace(",", "")),
            float(m.group(2).replace(",", "")),
            float(m.group(3).replace(",", "")),
        )
    nums = [float(x.replace(",", "")) for x in re.findall(r"(?:Buy|Sell|Hold)\s+([\d,]+\.\d+)", text)]
    nums = [n for n in nums if n > 0]
    if nums:
        return (min(nums), statistics.mean(nums), max(nums))
    return None


def parse_consensus_rating(text):
    """The 'Consensus %' shown on the site is NOT always Buy% - it's whichever
    of Buy/Hold/Sell% matches the overall Rating direction (confirmed by
    comparing live TipRanks data against the site's existing stored values,
    2026-09-05: e.g. a 'Hold' rating pairs with the HOLD%, not the BUY%)."""
    idx = text.find("ANALYST CONSENSUS")
    if idx == -1:
        return None
    snippet = text[idx: idx + 200]
    buy_m = re.search(r"BUY\s+(\d+)%", snippet)
    hold_m = re.search(r"HOLD\s+(\d+)%", snippet)
    sell_m = re.search(r"SELL\s+(\d+)%", snippet)
    rating_m = re.search(r"SELL\s+\d+%\s*\n\s*([A-Za-z ]+?)\s*\n\s*Based on", snippet)
    if not (buy_m and hold_m and sell_m and rating_m):
        return None
    rating = rating_m.group(1).strip()
    if "Sell" in rating:
        pct = sell_m.group(1)
    elif "Hold" in rating:
        pct = hold_m.group(1)
    else:
        pct = buy_m.group(1)
    return pct, rating


def parse_hedge_fund_activity(text):
    """The 'HEDGE FUND ACTIVITIES' table on the same TipRanks page (top ~3
    holders by value, e.g. Warren Buffett/Berkshire) shows each fund's most
    recent quarterly action: Added / Reduced / No change / New Position /
    Sold Out, plus the % holding change. Small sample size (only the
    default-visible top holders, not the full list) - treated as informal
    context, not scored into the Score total, same reasoning as P/E."""
    idx = text.find("HEDGE FUND ACTIVITIES")
    if idx == -1:
        return None
    end_idx = text.find("VIEW ALL", idx)
    if end_idx == -1:
        end_idx = idx + 1000
    snippet = text[idx:end_idx]
    matches = re.findall(r"(No change|Added|Reduced|New Position|Sold Out)\s+(-?[\d.]+)%", snippet)
    if not matches:
        return None
    added = sum(1 for a, _ in matches if a in ("Added", "New Position"))
    reduced = sum(1 for a, _ in matches if a in ("Reduced", "Sold Out"))
    unchanged = sum(1 for a, _ in matches if a == "No change")
    return added, reduced, unchanged, len(matches)


def load_all_rows():
    """Returns list of dicts: {file, lineno, ticker, name, price, low, avg, high, status, trade}"""
    rows = []
    files = sorted(f for f in glob.glob(str(ROOT / "analyst_targets_*.txt")) if "_OLD" not in f)
    for fname in files:
        lines = Path(fname).read_text(encoding="utf-8").split("\n")
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != 8:
                continue
            ticker, name, price, low, avg, high, status, trade = parts
            if status not in ("OK", "NOFAQ", "CVR"):
                continue
            rows.append({
                "file": fname, "lineno": i, "ticker": ticker, "name": name,
                "price": price, "low": low, "avg": avg, "high": high,
                "status": status, "trade": trade,
            })
    return rows


async def scan_one(context, sem, row, results, log_state):
    async with sem:
        ticker = row["ticker"]
        query_ticker = strip_suffix(ticker)
        page = await context.new_page()
        try:
            await page.goto(TIPRANKS_URL.format(query_ticker), wait_until="domcontentloaded", timeout=25000)
            await page.wait_for_timeout(3500)
            text = await page.inner_text("body")
            if "no research data" in text.lower():
                found = None
            else:
                idx = text.find("ANALYST PRICE TARGET")
                found = parse_low_avg_high(text[idx: idx + 600]) if idx != -1 else None
            cons_rating = parse_consensus_rating(text)
            if cons_rating:
                results["consensus"][ticker] = cons_rating
            hedge_fund = parse_hedge_fund_activity(text)
            if hedge_fund:
                results["hedgefund"][ticker] = hedge_fund
        except Exception as e:
            found = "ERROR"
        finally:
            await page.close()

        old_status = row["status"]
        if found == "ERROR":
            results["errors"].append(ticker)
        elif found is None:
            new_status = "NOFAQ" if old_status != "CVR" else "CVR"
            if old_status == "OK":
                results["lost_coverage"].append(ticker)
                row["status"] = "NOFAQ"
                row["low"] = row["avg"] = row["high"] = ""
                results["changed"].append(row)
            else:
                results["unchanged"].append(ticker)
        else:
            low, avg, high = found
            if old_status in ("NOFAQ",):
                results["new_green"].append(ticker)
                row["status"] = "OK"
                row["low"], row["avg"], row["high"] = f"{low:.2f}", f"{avg:.2f}", f"{high:.2f}"
                results["changed"].append(row)
            else:
                # still OK/CVR — refresh numbers
                row["low"], row["avg"], row["high"] = f"{low:.2f}", f"{avg:.2f}", f"{high:.2f}"
                results["refreshed"].append(ticker)
                results["changed"].append(row)

        log_state["done"] += 1
        if log_state["done"] % LOG_EVERY == 0:
            write_progress_log(log_state, results)


def write_progress_log(log_state, results):
    elapsed = time.time() - log_state["start"]
    rate = log_state["done"] / elapsed if elapsed > 0 else 0
    remaining = (log_state["total"] - log_state["done"]) / rate if rate > 0 else 0
    with open(ROOT / "MEGASCAN_LOG.md", "w", encoding="utf-8") as f:
        f.write(f"# MEGASCAN progress\n\n")
        f.write(f"Done: {log_state['done']} / {log_state['total']}\n\n")
        f.write(f"Elapsed: {elapsed/60:.1f} min | Rate: {rate:.2f}/s | ETA: {remaining/60:.1f} min\n\n")
        f.write(f"New green (yellow->green): {len(results['new_green'])}\n")
        f.write(f"Lost coverage (green->yellow): {len(results['lost_coverage'])}\n")
        f.write(f"Refreshed (still green): {len(results['refreshed'])}\n")
        f.write(f"Unchanged (still yellow): {len(results['unchanged'])}\n")
        f.write(f"Errors: {len(results['errors'])}\n")


def apply_changes(changed_rows):
    by_file = {}
    for row in changed_rows:
        by_file.setdefault(row["file"], []).append(row)

    for fname, rows in by_file.items():
        lines = Path(fname).read_text(encoding="utf-8").split("\n")
        for row in rows:
            fields = [row["ticker"], row["name"], row["price"], row["low"],
                      row["avg"], row["high"], row["status"], row["trade"]]
            lines[row["lineno"]] = "\t".join(fields)
        Path(fname).write_text("\n".join(lines), encoding="utf-8")


async def main():
    rows = load_all_rows()
    import os
    limit = os.environ.get("MEGASCAN_LIMIT")
    if limit:
        rows = rows[: int(limit)]
    print(f"Loaded {len(rows)} tickers to scan")

    results = {"new_green": [], "lost_coverage": [], "refreshed": [], "unchanged": [], "errors": [], "changed": [], "consensus": {}, "hedgefund": {}}
    log_state = {"done": 0, "total": len(rows), "start": time.time()}

    sem = asyncio.Semaphore(CONCURRENCY)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        tasks = [scan_one(context, sem, row, results, log_state) for row in rows]
        await asyncio.gather(*tasks)
        await browser.close()

    write_progress_log(log_state, results)

    print("Applying changes to analyst_targets_*.txt files...")
    apply_changes(results["changed"])

    print("Writing consensus_ratings.txt ...")
    with open(ROOT / "consensus_ratings.txt", "w", encoding="utf-8") as f:
        for ticker, (pct, rating) in results["consensus"].items():
            f.write(f"{ticker}\t{pct}\t{rating}\n")

    print("Writing hedge_fund_activity.tsv ...")
    with open(ROOT / "hedge_fund_activity.tsv", "w", encoding="utf-8") as f:
        for ticker, (added, reduced, unchanged, total) in results["hedgefund"].items():
            f.write(f"{ticker}\t{added}\t{reduced}\t{unchanged}\t{total}\n")

    print("Rebuilding site (build_site.py runs every merge script + reassembles)...")
    subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=False)

    with open(ROOT / "MEGASCAN_RESULTS.md", "w", encoding="utf-8") as f:
        f.write("# MEGASCAN Results\n\n")
        f.write(f"Total scanned: {len(rows)}\n\n")
        f.write(f"## New GREEN (yellow -> green, {len(results['new_green'])})\n")
        f.write(", ".join(results["new_green"]) + "\n\n")
        f.write(f"## Lost coverage (green -> yellow, {len(results['lost_coverage'])})\n")
        f.write(", ".join(results["lost_coverage"]) + "\n\n")
        f.write(f"## Refreshed numbers, still green ({len(results['refreshed'])})\n\n")
        f.write(f"## Still yellow, unchanged ({len(results['unchanged'])})\n\n")
        f.write(f"## Errors ({len(results['errors'])})\n")
        f.write(", ".join(results["errors"]) + "\n")

    print("MEGASCAN complete.")


if __name__ == "__main__":
    asyncio.run(main())
