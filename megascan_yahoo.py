"""
MEGASCAN YAHOO — full-exchange Yahoo Finance refresh (all 6,761 tickers).

Reduced scope vs. MEGASCAN (TipRanks): Yahoo Finance's current page layout no
longer shows a Low/Avg/High analyst-target breakdown anywhere (confirmed
2026-09-05, checked both /quote/{T} and /quote/{T}/analysis for AAPL) - only a
single "1y Target Est" average value. So this scans:
  - Average analyst price target (Yahoo's own single number)
  - Forward dividend yield %
for every ticker, via the same local headless-Chromium method as
megascan.py / portfolio_server.py (free, no LLM, no eToro involved at all -
this only touches finance.yahoo.com).

Run: python megascan_yahoo.py
Progress:  MEGASCAN_YAHOO_LOG.md (updated every 50 tickers)
Result:    MEGASCAN_YAHOO_RESULTS.md (written at the end)
"""

import asyncio
import glob
import re
import time
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
YAHOO_URL = "https://finance.yahoo.com/quote/{}"
CONCURRENCY = 5
LOG_EVERY = 50
# If no ticker finishes for this long, the browser is presumed hung (not
# crashed - is_connected() alone doesn't catch a browser that's technically
# alive but wedged, which is what actually froze this script for 50+ minutes
# on 2026-09-06). The watchdog force-closes it so the next get_page() call
# sees is_connected() == False and relaunches a fresh one.
WATCHDOG_IDLE_SECONDS = 90


def load_checkpoint():
    """Resumability: if a previous run left checkpoint files (crashed partway
    or was interrupted), load what's already scraped so a re-run skips those
    tickers instead of re-scanning the whole universe from scratch."""
    targets, dividends = {}, {}
    tf = ROOT / "yahoo_targets_0_MEGASCAN.txt"
    if tf.exists():
        for line in tf.read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 5:
                continue
            ticker, _, avg, _, currency = parts[:5]
            targets[ticker] = (float(avg) if avg else None, currency)
    df = ROOT / "yahoo_dividends_MEGASCAN.txt"
    if df.exists():
        for line in df.read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            dividends[parts[0]] = parts[1]
    return targets, dividends


def load_all_tickers():
    """Same ticker universe as megascan.py: every ticker across analyst_targets_*.txt."""
    tickers = []
    files = sorted(f for f in glob.glob(str(ROOT / "analyst_targets_*.txt")) if "_OLD" not in f)
    for fname in files:
        for line in Path(fname).read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != 8:
                continue
            tickers.append(parts[0])
    return tickers


async def dismiss_yahoo_consent(page, target_url):
    """Yahoo's consent wall is a full top-level redirect to consent.yahoo.com,
    not an overlay - clicking the reject button triggers a real navigation
    back to the original page, so the click must be wrapped in
    expect_navigation() or the page never leaves the consent domain."""
    for label in ("לדחות הכול", "Reject all", "לקבל הכול", "Accept all"):
        try:
            btn = page.locator(f"button:has-text('{label}')").first
            if await btn.count() == 0:
                continue
            try:
                async with page.expect_navigation(timeout=8000):
                    await btn.click(timeout=3000)
            except Exception:
                pass
            await page.wait_for_timeout(1000)
            return True
        except Exception:
            continue
    return False


def parse_target_and_div(text):
    target = None
    idx = text.find("1y Target Est")
    if idx != -1:
        m = re.search(r"1y Target Est\s*\n?([\d,]+\.?\d*)", text[idx: idx + 40])
        if m:
            try:
                target = float(m.group(1).replace(",", ""))
            except ValueError:
                pass

    div_pct = None
    idx = text.find("Forward Dividend & Yield")
    if idx != -1:
        snippet = text[idx: idx + 80]
        m = re.search(r"\(([\d.]+)%\)", snippet)
        if m:
            div_pct = m.group(1)
        else:
            div_pct = "0"

    currency = None
    m = re.search(r"\n([A-Z]{3})\n", text[:200])
    if m:
        currency = m.group(1)

    return target, div_pct, currency


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


async def scan_one(p, browser_state, lock, sem, ticker, results, log_state):
    async with sem:
        target = div_pct = currency = None
        success = False
        for attempt in range(2):
            page = None
            try:
                page = await get_page(p, browser_state, lock)
                url = YAHOO_URL.format(ticker)
                await page.goto(url, wait_until="domcontentloaded", timeout=25000)
                await page.wait_for_timeout(3000)
                text = await page.inner_text("body")
                if "consent.yahoo.com" in page.url or len(text) < 2000:
                    if await dismiss_yahoo_consent(page, url):
                        await page.wait_for_timeout(1500)
                        text = await page.inner_text("body")
                target, div_pct, currency = parse_target_and_div(text)
                success = True
                break
            except Exception:
                # First failure might just be a dead/wedged browser that's
                # about to get relaunched - retry once with a fresh page
                # before giving up on this ticker entirely.
                pass
            finally:
                if page is not None:
                    try:
                        await page.close()
                    except Exception:
                        pass  # a dead browser/driver connection must never abort the whole batch

        if not success:
            results["errors"].append(ticker)
        elif target is None and div_pct is None:
            results["no_data"].append(ticker)
        else:
            results["targets"][ticker] = (target, currency or "USD")
            if div_pct is not None:
                results["dividends"][ticker] = div_pct
            results["updated"].append(ticker)

        log_state["done"] += 1
        log_state["last_done_time"] = time.time()
        if log_state["done"] % LOG_EVERY == 0:
            write_progress_log(log_state, results)
            write_checkpoint(results)


async def watchdog(browser_state, lock, log_state):
    """Detects a browser that's alive but wedged - the failure mode that
    actually froze this script for 50+ minutes (is_connected() stayed True
    the whole time). If no ticker has completed in WATCHDOG_IDLE_SECONDS,
    force-close the current browser so the next get_page() call sees it as
    disconnected and relaunches a fresh one."""
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


def write_checkpoint(results):
    """Write partial results to disk periodically, so a mid-run crash (browser
    driver disconnect, host machine hiccup, etc.) doesn't lose everything -
    only whatever happened since the last checkpoint."""
    with open(ROOT / "yahoo_targets_0_MEGASCAN.txt", "w", encoding="utf-8") as f:
        for ticker, (target, currency) in results["targets"].items():
            avg = f"{target:.4f}" if target is not None else ""
            f.write(f"{ticker}\t\t{avg}\t\t{currency}\n")
    with open(ROOT / "yahoo_dividends_MEGASCAN.txt", "w", encoding="utf-8") as f:
        for ticker, div in results["dividends"].items():
            f.write(f"{ticker}\t{div}\n")


def write_progress_log(log_state, results):
    elapsed = time.time() - log_state["start"]
    rate = log_state["done"] / elapsed if elapsed > 0 else 0
    remaining = (log_state["total"] - log_state["done"]) / rate if rate > 0 else 0
    with open(ROOT / "MEGASCAN_YAHOO_LOG.md", "w", encoding="utf-8") as f:
        f.write("# MEGASCAN YAHOO progress\n\n")
        f.write(f"Done: {log_state['done']} / {log_state['total']}\n\n")
        f.write(f"Elapsed: {elapsed/60:.1f} min | Rate: {rate:.2f}/s | ETA: {remaining/60:.1f} min\n\n")
        f.write(f"Updated: {len(results['updated'])}\n")
        f.write(f"No data: {len(results['no_data'])}\n")
        f.write(f"Errors: {len(results['errors'])}\n")


async def main():
    all_tickers = load_all_tickers()
    import os
    limit = os.environ.get("MEGASCAN_YAHOO_LIMIT")
    if limit:
        all_tickers = all_tickers[: int(limit)]

    fresh = os.environ.get("MEGASCAN_YAHOO_FRESH")
    prev_targets, prev_dividends = ({}, {}) if fresh else load_checkpoint()
    already_done = set(prev_targets) | set(prev_dividends)
    tickers = [t for t in all_tickers if t not in already_done]
    print(f"Loaded {len(all_tickers)} tickers total, {len(already_done)} already done from a "
          f"previous checkpoint, {len(tickers)} left to scan")

    results = {
        "updated": [], "no_data": [], "errors": [],
        "targets": dict(prev_targets), "dividends": dict(prev_dividends),
    }
    log_state = {
        "done": 0, "total": len(tickers), "start": time.time(),
        "last_done_time": time.time(), "relaunches": 0, "finished": False,
    }

    if not tickers:
        print("Nothing left to scan - checkpoint already covers every ticker. "
              "Delete yahoo_targets_0_MEGASCAN.txt / yahoo_dividends_MEGASCAN.txt "
              "(or set MEGASCAN_YAHOO_FRESH=1) to force a full re-scan.")
        return

    sem = asyncio.Semaphore(CONCURRENCY)
    lock = asyncio.Lock()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        browser_state = {"browser": browser, "context": await browser.new_context()}

        # Warm-up: dismiss the Yahoo cookie wall once before going concurrent,
        # so the consent cookie is already in the shared context. Best-effort
        # only - if this hangs/fails (e.g. the browser is slow to come up),
        # every per-ticker scan_one() already has its own consent-dismiss
        # fallback, so skipping the warm-up just means the first few tickers
        # pay that cost individually instead of it being pre-paid once.
        try:
            warm = await get_page(p, browser_state, lock)
            warm_url = YAHOO_URL.format(tickers[0])
            await warm.goto(warm_url, wait_until="domcontentloaded", timeout=25000)
            await warm.wait_for_timeout(2000)
            if await dismiss_yahoo_consent(warm, warm_url):
                await warm.wait_for_timeout(1000)
            await warm.close()
        except Exception:
            pass

        watchdog_task = asyncio.create_task(watchdog(browser_state, lock, log_state))
        tasks = [scan_one(p, browser_state, lock, sem, t, results, log_state) for t in tickers]
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

    print("Writing yahoo_targets_0_MEGASCAN.txt and yahoo_dividends_MEGASCAN.txt ...")
    # Leading "0_" makes this sort alphabetically FIRST among yahoo_targets_*.txt
    # files (merge_yahoo_targets.py now loads them sorted), so any existing
    # per-exchange file with real scraped Low/High data overwrites this
    # avg-only fallback for its tickers, instead of the other way around.
    with open(ROOT / "yahoo_targets_0_MEGASCAN.txt", "w", encoding="utf-8") as f:
        for ticker, (target, currency) in results["targets"].items():
            avg = f"{target:.4f}" if target is not None else ""
            f.write(f"{ticker}\t\t{avg}\t\t{currency}\n")

    with open(ROOT / "yahoo_dividends_MEGASCAN.txt", "w", encoding="utf-8") as f:
        for ticker, div in results["dividends"].items():
            f.write(f"{ticker}\t{div}\n")

    print("Rebuilding site (build_site.py runs every merge script + reassembles)...")
    import subprocess
    import sys
    subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=False)

    still_missing = [t for t in all_tickers if t not in results["targets"] and t not in results["dividends"]]
    with open(ROOT / "MEGASCAN_YAHOO_RESULTS.md", "w", encoding="utf-8") as f:
        f.write("# MEGASCAN YAHOO Results\n\n")
        f.write(f"Full universe: {len(all_tickers)} | Scanned this run: {len(tickers)} "
                f"| Already had data before this run: {len(already_done)}\n\n")
        f.write(f"## Updated this run ({len(results['updated'])})\n\n")
        f.write(f"## No data ({len(results['no_data'])})\n")
        f.write(", ".join(results["no_data"]) + "\n\n")
        f.write(f"## Errors this run ({len(results['errors'])})\n")
        f.write(", ".join(results["errors"]) + "\n\n")
        f.write(f"## Still missing any data at all ({len(still_missing)})\n")
        if log_state.get("relaunches"):
            f.write(f"**The browser was relaunched {log_state['relaunches']} time(s) during this run** "
                    "(crashed or went unresponsive) - handled automatically, no data should be lost. "
                    "Progress is checkpointed regardless - just re-run `python megascan_yahoo.py` to "
                    f"pick up only the {len(still_missing)} tickers still missing, not start over.\n")

    print(f"MEGASCAN YAHOO complete. {len(still_missing)} tickers still have no data at all "
          f"out of {len(all_tickers)} - re-run the script to pick those up if that number is > 0.")


if __name__ == "__main__":
    asyncio.run(main())
