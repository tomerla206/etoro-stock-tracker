"""
SCAN VALUES — full refresh, but scoped to HELD tickers only (portfolio_virtual.tsv +
portfolio_real.tsv). Fast (~1-2 min, ~55 tickers) because it's the same per-ticker work
as MEGASCAN / MEGASCAN YAHOO / INSIDER SCAN, just run against a tiny ticker list instead
of the full 6,356-ticker universe.

Refreshes, for each held ticker:
  - TipRanks: Low/Avg/High analyst target (eToro/TipRanks side) + Consensus %/Rating
  - Yahoo Finance: dividend yield + 1y Target Est average (+ currency)
  - SEC EDGAR: insider buy/sell activity (last 30 days, open-market P/S only)

Reuses the exact same parsing/fetch functions as megascan.py / megascan_yahoo.py /
insider_scan.py (imported, not duplicated) so the two logic paths (full-universe vs.
held-only) can never silently drift apart.

Progress: SCAN_VALUES_LOG.md (written at start and end - too fast to need
periodic checkpointing like the full-universe scans).
"""

import glob
import re
import statistics
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
TIPRANKS_URL = "https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={}&theme=light"
YAHOO_URL = "https://finance.yahoo.com/quote/{}"
SUFFIX_STRIP = (".US", ".A", ".B", ".EUR")


def write_log(status, done=0, total=0, extra=""):
    with open(ROOT / "SCAN_VALUES_LOG.md", "w", encoding="utf-8") as f:
        f.write("# SCAN VALUES progress\n\n")
        f.write(f"Status: {status}\n\n")
        if total:
            f.write(f"Done: {done} / {total}\n\n")
        f.write(f"Updated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        if extra:
            f.write(f"\n{extra}\n")


def load_portfolio_tickers():
    tickers = set()
    for fname in ("portfolio_virtual.tsv", "portfolio_real.tsv"):
        path = ROOT / fname
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) >= 8 and parts[7].strip() == "HELD":
                tickers.add(parts[0].strip())
    return sorted(tickers)


def find_ticker_file(ticker):
    for fname in glob.glob(str(ROOT / "analyst_targets_*.txt")):
        if "_OLD" in fname:
            continue
        with open(fname, encoding="utf-8") as f:
            for line in f:
                if line.split("\t", 1)[0] == ticker:
                    return fname
    return None


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
        text, re.S,
    )
    if m:
        return (float(m.group(1).replace(",", "")), float(m.group(2).replace(",", "")), float(m.group(3).replace(",", "")))
    nums = [float(x.replace(",", "")) for x in re.findall(r"(?:Buy|Sell|Hold)\s+([\d,]+\.\d+)", text)]
    nums = [n for n in nums if n > 0]
    if nums:
        return (min(nums), statistics.mean(nums), max(nums))
    return None


def scan_tipranks(page, ticker, cons_results):
    query_ticker = strip_suffix(ticker)
    page.goto(TIPRANKS_URL.format(query_ticker), wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    text = page.inner_text("body")

    from megascan import parse_consensus_rating
    cons_rating = parse_consensus_rating(text)
    if cons_rating:
        cons_results[ticker] = cons_rating

    if "no research data" in text.lower():
        return None
    idx = text.find("ANALYST PRICE TARGET")
    if idx == -1:
        return None
    return parse_low_avg_high(text[idx: idx + 600])


def dismiss_yahoo_consent(page, target_url):
    """Yahoo's consent wall is a full top-level redirect to consent.yahoo.com,
    not an overlay - the click must be wrapped in expect_navigation() or the
    page never actually leaves the consent domain. Mirrors megascan_yahoo.py's
    logic exactly (a prior version here silently marked itself 'done' even on
    failure, permanently skipping every ticker after the first)."""
    for label in ("לדחות הכול", "Reject all", "לקבל הכול", "Accept all"):
        try:
            btn = page.locator(f"button:has-text('{label}')").first
            if btn.count() == 0:
                continue
            try:
                with page.expect_navigation(timeout=8000):
                    btn.click(timeout=3000)
            except Exception:
                pass
            page.wait_for_timeout(1000)
            return True
        except Exception:
            continue
    return False


def scan_yahoo(page, ticker):
    """Returns (div_pct, target_avg, currency), or (None, None, None) if the
    consent wall couldn't be cleared - callers must skip updating on None
    rather than writing a blank/zero over previously-good data."""
    url = YAHOO_URL.format(ticker)
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2000)
    text = page.inner_text("body")
    if "consent.yahoo.com" in page.url or len(text) < 2000:
        if dismiss_yahoo_consent(page, url):
            page.wait_for_timeout(1500)
            text = page.inner_text("body")
    if "consent.yahoo.com" in page.url or len(text) < 2000:
        return None, None, None

    from megascan_yahoo import parse_target_and_div
    target, div_pct, currency = parse_target_and_div(text)
    return div_pct, target, currency or "USD"


def update_analyst_file(ticker, low, avg, high):
    fname = find_ticker_file(ticker)
    if not fname:
        return False
    lines = Path(fname).read_text(encoding="utf-8").split("\n")
    changed = False
    for i, line in enumerate(lines):
        parts = line.split("\t")
        if parts and parts[0] == ticker and len(parts) >= 8:
            parts[3] = f"{low:.2f}"
            parts[4] = f"{avg:.2f}"
            parts[5] = f"{high:.2f}"
            lines[i] = "\t".join(parts)
            changed = True
            break
    if changed:
        Path(fname).write_text("\n".join(lines), encoding="utf-8")
    return changed


def update_dividend_file(results):
    path = ROOT / "yahoo_dividends_PORTFOLIO.txt"
    existing = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                existing[parts[0]] = parts[1]
    existing.update(results)
    with open(path, "w", encoding="utf-8") as f:
        for t, v in existing.items():
            f.write(f"{t}\t{v}\n")


def update_yahoo_targets_file(results):
    """yahoo_targets_PORTFOLIO.txt - sorts alphabetically after
    yahoo_targets_0_MEGASCAN.txt, so merge_yahoo_targets.py lets these
    fresher held-ticker values win over the full-universe fallback."""
    path = ROOT / "yahoo_targets_PORTFOLIO.txt"
    existing = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) >= 5:
                existing[parts[0]] = parts[1:5]
    for ticker, (target, currency) in results.items():
        avg = f"{target:.4f}" if target is not None else ""
        existing[ticker] = ["", avg, "", currency]
    with open(path, "w", encoding="utf-8") as f:
        for t, parts in existing.items():
            f.write(f"{t}\t{parts[0]}\t{parts[1]}\t{parts[2]}\t{parts[3]}\n")


def update_consensus_file(results):
    path = ROOT / "consensus_ratings.txt"
    existing = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) == 3:
                existing[parts[0]] = (parts[1], parts[2])
    existing.update(results)
    with open(path, "w", encoding="utf-8") as f:
        for t, (pct, rating) in existing.items():
            f.write(f"{t}\t{pct}\t{rating}\n")


def scan_insider(tickers):
    """Same SEC EDGAR method as insider_scan.py, reused directly - only run
    against the held tickers, so it takes well under a second."""
    from insider_scan import load_cik_map, fetch_json, fetch_text, parse_form4_transactions
    import concurrent.futures

    cik_map = load_cik_map()
    matched = [(t, cik_map[t]) for t in tickers if t in cik_map]
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    activity = {}

    def scan_one(ticker, cik):
        cik_padded = f"{cik:010d}"
        sub = fetch_json(f"https://data.sec.gov/submissions/CIK{cik_padded}.json")
        if not sub:
            return
        recent = sub.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accns = recent.get("accessionNumber", [])
        docs = recent.get("primaryDocument", [])

        buy_total, sell_total, buy_count, sell_count = 0.0, 0.0, 0, 0
        for i, form in enumerate(forms):
            if form != "4" or dates[i] < cutoff:
                continue
            accn_nodash = accns[i].replace("-", "")
            raw_name = docs[i].split("/")[-1]
            xml_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn_nodash}/{raw_name}"
            text = fetch_text(xml_url)
            if not text:
                continue
            for code, shares, price in parse_form4_transactions(text):
                if code == "P":
                    buy_total += shares * price
                    buy_count += 1
                elif code == "S":
                    sell_total += shares * price
                    sell_count += 1

        if buy_count or sell_count:
            activity[ticker] = {"buy": buy_total, "sell": sell_total, "buy_count": buy_count, "sell_count": sell_count}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = [ex.submit(scan_one, t, cik) for t, cik in matched]
        concurrent.futures.wait(futures)

    return activity


def update_insider_file(activity):
    path = ROOT / "insider_activity.tsv"
    existing = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) == 6:
                existing[parts[0]] = parts[1:]
    for ticker, a in activity.items():
        net = a["buy"] - a["sell"]
        existing[ticker] = [f"{net:.0f}", f"{a['buy']:.0f}", f"{a['sell']:.0f}", str(a["buy_count"]), str(a["sell_count"])]
    with open(path, "w", encoding="utf-8") as f:
        for t, parts in existing.items():
            f.write(f"{t}\t" + "\t".join(parts) + "\n")


def main():
    from playwright.sync_api import sync_playwright

    tickers = load_portfolio_tickers()
    if not tickers:
        write_log("error: no HELD tickers found")
        print("No HELD tickers found in portfolio files.")
        return

    write_log("running", 0, len(tickers))
    updated, unchanged, no_data, dividends, yahoo_targets, cons_results = [], [], [], {}, {}, {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for i, ticker in enumerate(tickers):
            try:
                result = scan_tipranks(page, ticker, cons_results)
                if result:
                    low, avg, high = result
                    (updated if update_analyst_file(ticker, low, avg, high) else unchanged).append(ticker)
                else:
                    no_data.append(ticker)
            except Exception as e:
                no_data.append(f"{ticker} (error: {e})")

            try:
                div_pct, yh_target, yh_currency = scan_yahoo(page, ticker)
                if div_pct is not None:
                    dividends[ticker] = div_pct
                if yh_target is not None:
                    yahoo_targets[ticker] = (yh_target, yh_currency)
            except Exception:
                pass

            write_log("running", i + 1, len(tickers))
        browser.close()

    print("Running insider scan (SEC EDGAR) for held tickers...")
    activity = scan_insider(tickers)

    update_dividend_file(dividends)
    update_yahoo_targets_file(yahoo_targets)
    update_consensus_file(cons_results)
    update_insider_file(activity)

    print("Rebuilding site (build_site.py runs every merge script + reassembles)...")
    subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=False)

    write_log(
        "done", len(tickers), len(tickers),
        extra=(
            f"TipRanks - Updated: {len(updated)} | Unchanged: {len(unchanged)} | No data: {len(no_data)}\n\n"
            f"Consensus/Rating refreshed: {len(cons_results)}\n\n"
            f"Yahoo dividends: {len(dividends)} | Yahoo targets: {len(yahoo_targets)}\n\n"
            f"Insider activity found: {len(activity)} (of {len(tickers)} held tickers checked)"
        ),
    )
    print(f"SCAN VALUES complete: {len(updated)} TipRanks updated, {len(cons_results)} consensus refreshed, "
          f"{len(yahoo_targets)} Yahoo targets, {len(activity)} tickers with insider activity")


if __name__ == "__main__":
    main()
