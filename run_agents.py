import os
import sys
import time
import random
import glob
import json
import urllib.request

# Configuration according to PROJECT_LOG.md policy
DELAYS_PER_TICKER = (3, 8)        # Randomized 3-8s wait per ticker
BATCH_SIZE = (12, 15)              # 12-15 tickers per batch
BATCH_PAUSE = (30, 50)             # 30-50s pause between batches
DATA_FILE = "nasdaq_data.tsv"
CDP_PORT = 9222

def load_master_data():
    """Load master tickers and company names from nasdaq_data.tsv"""
    master = {}
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
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

def load_completed_tickers():
    """Load all already processed tickers across analyst_targets_*.txt"""
    completed = set()
    for filepath in glob.glob("analyst_targets_*.txt"):
        if "_OLD" in filepath:
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if parts:
                    completed.add(parts[0])
    return completed

def get_letter_worklist(letter, master_data, completed_set):
    """Get remaining tickers for a specific letter"""
    all_letter_tickers = [t for t in master_data.keys() if t.upper().startswith(letter.upper())]
    all_letter_tickers.sort()
    remaining = [t for t in all_letter_tickers if t not in completed_set]
    return remaining

def check_cdp_status():
    """Check if Chrome is running with --remote-debugging-port=9222"""
    try:
        url = f"http://localhost:{CDP_PORT}/json/version"
        req = urllib.request.urlopen(url, timeout=3)
        data = json.loads(req.read().decode())
        print(f"Connected to Chrome! Browser: {data.get('Browser', 'Chrome')}")
        return True
    except Exception as e:
        print(f"Chrome CDP not detected on port {CDP_PORT} ({e}).")
        print("Please start Chrome with: chrome.exe --remote-debugging-port=9222")
        return False

def main():
    print("=" * 60)
    print("  NASDAQ Stock List - Dual Agent Automation Runner")
    print("=" * 60)
    
    master_data = load_master_data()
    completed = load_completed_tickers()
    
    print(f"Master dataset: {len(master_data)} tickers loaded.")
    print(f"Completed tickers so far: {len(completed)}.")
    
    # R worklist (Forward)
    r_rem = get_letter_worklist("R", master_data, completed)
    print(f"Letter R remaining ({len(r_rem)} tickers): {r_rem[:5]} ...")
    
    # X worklist (Backward)
    x_rem = get_letter_worklist("X", master_data, completed)
    print(f"Letter X remaining ({len(x_rem)} tickers): {x_rem[:5]} ...")
    
    is_cdp_ready = check_cdp_status()
    if not is_cdp_ready:
        print("\n[!] Chrome is not running in debugging mode yet.")
        print("    Run this command in Windows (Win + R):")
        print(f"    chrome.exe --remote-debugging-port={CDP_PORT}")
        print("    Then log into eToro and re-run this script.")
        return

    print("\n[+] System ready! You can now launch Playwright / Selenium / CDP runner.")

if __name__ == "__main__":
    main()
