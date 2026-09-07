"""
INSIDER SCAN — insider buying/selling activity via SEC EDGAR (Form 4 filings).

Free, public, no login, no browser needed at all (pure JSON/XML HTTP requests,
much lighter than the Playwright-based scans). Coverage is necessarily partial:
only US-domestic SEC-reporting issuers file Form 4 - foreign private issuers
(most non-US-exchange tickers, many ADRs) are exempt from Section 16 reporting
and will simply have no data, which is expected and not an error.

Method:
1. Map ticker -> CIK via SEC's public company_tickers.json.
2. For each matched ticker, fetch its EDGAR submissions.json, find Form 4
   filings from the last LOOKBACK_DAYS days.
3. For each such filing, fetch the raw ownershipDocument XML and sum up
   OPEN-MARKET transactions only (transactionCode 'P' = purchase, 'S' = sale -
   excludes grants/awards/option-exercises/gifts/tax-withholding, which aren't
   a real buy/sell conviction signal).
4. Classify each ticker: net $ bought vs sold in the window.

SEC's fair-access policy requires a real, identifying User-Agent and asks for
<=10 requests/second - both respected here (8 worker threads, one request in
flight per worker at a time).

Run: python insider_scan.py
Progress:  INSIDER_SCAN_LOG.md
Result:    INSIDER_SCAN_RESULTS.md, insider_activity.tsv (TICKER, net $, buys, sells)
"""

import concurrent.futures
import glob
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).parent
HEADERS = {"User-Agent": "eToroStockTracker research contact@example.com"}
LOOKBACK_DAYS = 30
WORKERS = 8
LOG_EVERY = 100


def load_all_tickers():
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


def load_cik_map():
    resp = requests.get("https://www.sec.gov/files/company_tickers.json", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return {row["ticker"]: row["cik_str"] for row in data.values()}


def fetch_json(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    if resp.status_code != 200:
        return None
    return resp.json()


def fetch_text(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    if resp.status_code != 200:
        return None
    return resp.text


def parse_form4_transactions(xml_text):
    """Returns list of (code, shares, price) for open-market P/S transactions only."""
    out = []
    for block in re.findall(r"<nonDerivativeTransaction>.*?</nonDerivativeTransaction>", xml_text, re.S):
        code_m = re.search(r"<transactionCode>([A-Z])</transactionCode>", block)
        if not code_m or code_m.group(1) not in ("P", "S"):
            continue
        shares_m = re.search(r"<transactionShares>\s*<value>([\d.]+)</value>", block)
        price_m = re.search(r"<transactionPricePerShare>\s*<value>([\d.]+)</value>", block)
        if not shares_m or not price_m:
            continue
        out.append((code_m.group(1), float(shares_m.group(1)), float(price_m.group(1))))
    return out


def scan_one(ticker, cik, cutoff_date, results, log_state):
    try:
        cik_padded = f"{cik:010d}"
        sub = fetch_json(f"https://data.sec.gov/submissions/CIK{cik_padded}.json")
        if not sub:
            results["no_data"].append(ticker)
            return
        recent = sub.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accns = recent.get("accessionNumber", [])
        docs = recent.get("primaryDocument", [])

        buy_total, sell_total, buy_count, sell_count = 0.0, 0.0, 0, 0
        for i, form in enumerate(forms):
            if form != "4":
                continue
            if dates[i] < cutoff_date:
                continue
            accn_nodash = accns[i].replace("-", "")
            doc_name = docs[i]
            # The primaryDocument is often the rendered xslF345X06/form4.xml;
            # the raw ownershipDocument XML lives at the same accession folder
            # under just the filename (no xsl subfolder).
            raw_name = doc_name.split("/")[-1]
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

        if buy_count == 0 and sell_count == 0:
            results["no_activity"].append(ticker)
        else:
            results["activity"][ticker] = {
                "buy": buy_total, "sell": sell_total,
                "buy_count": buy_count, "sell_count": sell_count,
            }
            results["updated"].append(ticker)
    except Exception:
        results["errors"].append(ticker)
    finally:
        log_state["done"] += 1
        if log_state["done"] % LOG_EVERY == 0:
            write_progress_log(log_state, results)


def write_progress_log(log_state, results):
    elapsed = time.time() - log_state["start"]
    rate = log_state["done"] / elapsed if elapsed > 0 else 0
    remaining = (log_state["total"] - log_state["done"]) / rate if rate > 0 else 0
    with open(ROOT / "INSIDER_SCAN_LOG.md", "w", encoding="utf-8") as f:
        f.write("# INSIDER SCAN progress\n\n")
        f.write(f"Done: {log_state['done']} / {log_state['total']}\n\n")
        f.write(f"Elapsed: {elapsed/60:.1f} min | Rate: {rate:.2f}/s | ETA: {remaining/60:.1f} min\n\n")
        f.write(f"Tickers with recent insider activity: {len(results['activity'])}\n")
        f.write(f"No CIK match (non-US/foreign issuer): {log_state.get('no_cik', 0)}\n")
        f.write(f"CIK matched, no recent Form 4: {len(results['no_activity']) + len(results['no_data'])}\n")
        f.write(f"Errors: {len(results['errors'])}\n")


def main():
    tickers = load_all_tickers()
    import os
    limit = os.environ.get("INSIDER_SCAN_LIMIT")
    if limit:
        tickers = tickers[: int(limit)]
    print(f"Loaded {len(tickers)} tickers")

    print("Fetching SEC ticker->CIK map...")
    cik_map = load_cik_map()
    matched = [(t, cik_map[t]) for t in tickers if t in cik_map]
    no_cik = len(tickers) - len(matched)
    print(f"{len(matched)} tickers matched a CIK ({no_cik} have no SEC filer - expected for non-US listings)")

    cutoff = (datetime.now() - timedelta(days=LOOKBACK_DAYS)).strftime("%Y-%m-%d")
    results = {"updated": [], "no_activity": [], "no_data": [], "errors": [], "activity": {}}
    log_state = {"done": 0, "total": len(matched), "start": time.time(), "no_cik": no_cik}

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = [ex.submit(scan_one, t, cik, cutoff, results, log_state) for t, cik in matched]
        concurrent.futures.wait(futures)

    write_progress_log(log_state, results)

    print("Writing insider_activity.tsv ...")
    with open(ROOT / "insider_activity.tsv", "w", encoding="utf-8") as f:
        for ticker, a in results["activity"].items():
            net = a["buy"] - a["sell"]
            f.write(f"{ticker}\t{net:.0f}\t{a['buy']:.0f}\t{a['sell']:.0f}\t{a['buy_count']}\t{a['sell_count']}\n")

    with open(ROOT / "INSIDER_SCAN_RESULTS.md", "w", encoding="utf-8") as f:
        f.write("# INSIDER SCAN Results\n\n")
        f.write(f"Tickers checked: {len(matched)} (of {len(tickers)} total; {no_cik} have no US SEC filer)\n\n")
        f.write(f"## Tickers with recent insider activity ({len(results['activity'])})\n\n")
        top_buys = sorted(results["activity"].items(), key=lambda kv: kv[1]["buy"] - kv[1]["sell"], reverse=True)[:20]
        f.write("### Top net buying\n")
        for t, a in top_buys:
            f.write(f"- {t}: net ${a['buy']-a['sell']:,.0f} ({a['buy_count']} buys, {a['sell_count']} sells)\n")
        top_sells = sorted(results["activity"].items(), key=lambda kv: kv[1]["buy"] - kv[1]["sell"])[:20]
        f.write("\n### Top net selling\n")
        for t, a in top_sells:
            f.write(f"- {t}: net ${a['buy']-a['sell']:,.0f} ({a['buy_count']} buys, {a['sell_count']} sells)\n")
        f.write(f"\n## Errors ({len(results['errors'])})\n")
        f.write(", ".join(results["errors"]) + "\n")

    print("Rebuilding site (build_site.py runs every merge script + reassembles)...")
    import subprocess
    import sys
    subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=False)

    print("INSIDER SCAN complete.")


if __name__ == "__main__":
    main()
