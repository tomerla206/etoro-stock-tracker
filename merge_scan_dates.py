import re
import glob
import os
from datetime import datetime, timezone

ROWS_FILE = "all_rows.html"

def load_ticker_dates():
    ticker_date = {}
    files = [f for f in glob.glob("analyst_targets_*.txt") if 'OLD' not in f and 'backup' not in f]
    for fp in files:
        mtime = os.path.getmtime(fp)
        date_str = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
        with open(fp, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line.strip():
                    continue
                ticker = line.split('\t')[0].strip()
                if ticker:
                    ticker_date[ticker] = date_str
    return ticker_date

def main():
    ticker_date = load_ticker_dates()
    with open(ROWS_FILE, encoding='utf-8') as f:
        html = f.read()

    matched = 0
    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        # strip previously-injected attr (idempotent re-run)
        tr_open = re.sub(r'\s*data-scandate="[^"]*"', '', tr_open)
        date_str = ticker_date.get(ticker)
        if not date_str:
            return tr_open
        matched += 1
        return tr_open[:-1] + f' data-scandate="{date_str}">'

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    with open(ROWS_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Scan dates merged: {matched} rows tagged (out of {len(ticker_date)} known tickers from {len(set(ticker_date.values()))} distinct dates).")

if __name__ == '__main__':
    main()
