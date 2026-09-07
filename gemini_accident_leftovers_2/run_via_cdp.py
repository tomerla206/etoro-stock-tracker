import os
import sys
import time
import random
import glob
import re
import urllib.request
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(line_buffering=True)
DATA_FILE = "nasdaq_data.tsv"
CDP_URL = "http://localhost:9222"

def print_log(msg):
    print(msg, flush=True)

def load_master_data():
    master = {}
    if not os.path.exists(DATA_FILE):
        print_log(f"Error: {DATA_FILE} not found.")
        sys.exit(1)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("TICKER"):
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                ticker = parts[0]
                name = parts[1]
                price = parts[2]
                master[ticker] = {"name": name, "price": price}
    return master

def load_completed_tickers(letter):
    filepath = f"analyst_targets_{letter}.txt"
    completed = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if parts:
                    completed[parts[0]] = line
    return completed

def append_target(letter, line):
    filepath = f"analyst_targets_{letter}.txt"
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def process_ticker(page, ticker, company_name, current_price):
    url = f"https://www.etoro.com/markets/{ticker.lower()}/research"
    print_log(f" -> Moving existing Chrome tab to: {url}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        print_log(f"    Navigation warning for {ticker}: {e}")
        
    time.sleep(random.uniform(3.5, 6.0))

    try:
        page_text = page.inner_text("body")
    except Exception:
        page_text = ""

    if "Error 1015" in page_text or "rate limited" in page_text.lower():
        return "BLOCKED", None

    trade_status = "NOT_TRADEABLE"
    try:
        trade_btn = page.query_selector("button:has-text('Trade'), button:has-text('מסחר')")
        if trade_btn and trade_btn.is_visible():
            trade_status = "TRADEABLE"
    except Exception:
        pass

    if "no research data" in page_text.lower() or "has no research data" in page_text.lower():
        res_line = f"{ticker}\t{company_name}\t{current_price}\t\t\t\tNOFAQ\t{trade_status}"
        return "OK", res_line

    low, avg, high = "", "", ""
    try:
        matches = re.findall(r"\$(\d+\.\d{2})", page_text)
        if len(matches) >= 3:
            low, avg, high = matches[0], matches[1], matches[2]
            status = "OK"
        else:
            status = "NOFAQ"
    except Exception:
        status = "NOFAQ"

    res_line = f"{ticker}\t{company_name}\t{current_price}\t{low}\t{avg}\t{high}\t{status}\t{trade_status}"
    return "OK", res_line

def run_agent_for_letter(page, letter, master_data):
    completed_dict = load_completed_tickers(letter)
    worklist = [t for t in sorted(master_data.keys()) if t.upper().startswith(letter.upper()) and t not in completed_dict]
    
    print_log(f"\n==========================================")
    print_log(f" Starting CDP Agent for Letter {letter}")
    print_log(f" Remaining tickers: {len(worklist)}")
    print_log(f"==========================================\n")

    if not worklist:
        print_log(f"[!] Letter {letter} is already 100% completed!")
        return True

    batch_count = 0
    for i, ticker in enumerate(worklist, 1):
        info = master_data[ticker]
        print_log(f"[{letter}] ({i}/{len(worklist)}) Moving Chrome tab to {ticker} ({info['name']})...")
        
        status, line = process_ticker(page, ticker, info['name'], info['price'])
        if status == "BLOCKED":
            print_log(f"[!] BLOCKED detected on ticker {ticker}. Stopping agent for letter {letter}.")
            return False

        append_target(letter, line)
        print_log(f"    -> Saved: {line}")
        batch_count += 1

        delay = random.uniform(3.0, 8.0)
        time.sleep(delay)

        if batch_count >= random.randint(12, 15):
            pause_time = random.uniform(30.0, 50.0)
            print_log(f"--- Batch checkpoint reached ({batch_count} tickers). Pausing {pause_time:.1f}s ---")
            time.sleep(pause_time)
            batch_count = 0

    print_log(f"\n[SUCCESS] Letter {letter} completed fully!")
    return True

def main():
    # Check if Chrome CDP is available
    try:
        urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=2)
        print_log("[+] Chrome CDP detected on port 9222!")
    except Exception:
        print_log("[!] Chrome CDP not active on port 9222.")
        print_log("    Please start Chrome with: chrome.exe --remote-debugging-port=9222")
        return

    master_data = load_master_data()
    
    with sync_playwright() as p:
        print_log("Connecting Playwright directly to your open Chrome browser...")
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()

        # Run Letter R agent (Forward) using your open Chrome tab directly!
        print_log("Starting Letter R worker...")
        run_agent_for_letter(page, "R", master_data)
        
        # Run Letter X agent (Backward)
        print_log("Starting Letter X worker...")
        run_agent_for_letter(page, "X", master_data)

if __name__ == "__main__":
    main()
