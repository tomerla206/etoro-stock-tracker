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
import json
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
# If no ticker finishes for this long, the browser is presumed hung (not
# crashed - is_connected() alone doesn't catch a browser that's technically
# alive but wedged). The watchdog force-closes it so the next get_page() call
# sees is_connected() == False and relaunches a fresh one.
WATCHDOG_IDLE_SECONDS = 90


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


async def relaunch_browser(p, browser_state, lock):
    """Swap in a fresh browser+context, closing the old (possibly dead/hung)
    one best-effort. Guarded by a lock so that when several concurrent tasks
    all notice a dead browser at the same moment, only one of them actually
    relaunches - the rest just pick up the new browser_state once they get
    the lock."""
    async with lock:
        old_browser = browser_state.get("browser")
        if old_browser is not None and old_browser.is_connected():
            return  # someone else already relaunched while we waited for the lock
        if old_browser is not None:
            try:
                await old_browser.close()
            except Exception:
                pass
        new_browser = await p.chromium.launch(headless=True)
        browser_state["browser"] = new_browser
        browser_state["context"] = await new_browser.new_context()


async def get_page(p, browser_state, lock):
    """Open a new page, relaunching the browser first if it's no longer
    connected (a crashed process). context.new_page() itself still has no
    timeout of its own, so it's bounded here too - a browser that's alive but
    wedged (not crashed) won't be caught by is_connected(); that case is
    handled separately by the watchdog task, which force-closes a stalled
    browser so this check starts firing for it too."""
    if not browser_state["browser"].is_connected():
        await relaunch_browser(p, browser_state, lock)
    return await asyncio.wait_for(browser_state["context"].new_page(), timeout=15)


async def watchdog(browser_state, lock, log_state):
    """Detects a browser that's alive but wedged (is_connected() alone would
    stay True the whole time). If no ticker has completed in
    WATCHDOG_IDLE_SECONDS, force-close the current browser so the next
    get_page() call sees it as disconnected and relaunches a fresh one."""
    while not log_state["finished"]:
        await asyncio.sleep(15)
        if log_state["done"] >= log_state["total"]:
            break
        idle = time.time() - log_state["last_done_time"]
        if idle > WATCHDOG_IDLE_SECONDS:
            log_state["relaunches"] = log_state.get("relaunches", 0) + 1
            async with lock:
                browser = browser_state.get("browser")
                if browser is not None:
                    try:
                        await browser.close()
                    except Exception:
                        pass
            log_state["last_done_time"] = time.time()  # don't refire every 15s while relaunch is in flight


async def scan_one(p, browser_state, lock, sem, row, results, log_state):
    async with sem:
        ticker = row["ticker"]
        query_ticker = strip_suffix(ticker)
        found = "ERROR"
        for attempt in range(2):
            page = None
            try:
                page = await get_page(p, browser_state, lock)
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
                break
            except Exception:
                # First failure might just be a dead/wedged browser that's
                # about to get relaunched - retry once with a fresh page
                # before giving up on this ticker entirely.
                found = "ERROR"
            finally:
                if page is not None:
                    try:
                        await page.close()
                    except Exception:
                        pass  # a dead browser/driver connection must never abort the whole batch

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
        log_state["last_done_time"] = time.time()
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


def write_shard_output(shard_index, results):
    """Parallel cloud mode (SHARD_COUNT > 1): each shard only scans its own
    slice of tickers and can't safely touch the shared analyst_targets_*.txt
    files or run build_site.py itself (concurrent shards would race on the
    same files) - it just drops its results as JSON for aggregate_scan_shards.py
    to combine once every shard is done."""
    out_dir = ROOT / "shard_out"
    out_dir.mkdir(exist_ok=True)
    payload = {
        "changed": results["changed"], "consensus": results["consensus"],
        "hedgefund": results["hedgefund"], "new_green": results["new_green"],
        "lost_coverage": results["lost_coverage"], "refreshed": results["refreshed"],
        "unchanged": results["unchanged"], "errors": results["errors"],
    }
    with open(out_dir / f"megascan_shard{shard_index}.json", "w", encoding="utf-8") as f:
        json.dump(payload, f)


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

    # Parallel cloud mode: SHARD_COUNT > 1 means this is one of several
    # concurrent GitHub Actions jobs each covering a slice of the full
    # universe. Slicing with a stride (not contiguous chunks) spreads any
    # clustering in the source files (e.g. all-.HK tickers grouped together)
    # evenly across shards instead of giving one shard all the slow ones.
    shard_index = int(os.environ.get("SHARD_INDEX", "0"))
    shard_count = int(os.environ.get("SHARD_COUNT", "1"))
    if shard_count > 1:
        rows = rows[shard_index::shard_count]
        print(f"Shard {shard_index}/{shard_count}: {len(rows)} tickers assigned")
    print(f"Loaded {len(rows)} tickers to scan")

    results = {"new_green": [], "lost_coverage": [], "refreshed": [], "unchanged": [], "errors": [], "changed": [], "consensus": {}, "hedgefund": {}}
    log_state = {
        "done": 0, "total": len(rows), "start": time.time(),
        "last_done_time": time.time(), "relaunches": 0, "finished": False,
    }

    sem = asyncio.Semaphore(CONCURRENCY)
    lock = asyncio.Lock()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        browser_state = {"browser": browser, "context": await browser.new_context()}
        watchdog_task = asyncio.create_task(watchdog(browser_state, lock, log_state))
        tasks = [scan_one(p, browser_state, lock, sem, row, results, log_state) for row in rows]
        await asyncio.gather(*tasks, return_exceptions=True)
        log_state["finished"] = True
        watchdog_task.cancel()
        try:
            await watchdog_task
        except asyncio.CancelledError:
            pass
        try:
            await browser_state["browser"].close()
        except Exception:
            pass

    write_progress_log(log_state, results)
    if log_state["relaunches"]:
        print(f"Browser was relaunched {log_state['relaunches']} time(s) during this run "
              "(crashed or went unresponsive) - handled automatically.")

    if shard_count > 1:
        write_shard_output(shard_index, results)
        print(f"Shard {shard_index} complete - wrote shard_out/megascan_shard{shard_index}.json "
              "(aggregate_scan_shards.py applies changes/rebuilds the site once every shard is done).")
        return

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
