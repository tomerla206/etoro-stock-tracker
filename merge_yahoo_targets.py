import re
import glob

ROWS_FILE = "all_rows.html"

# Kept in each ticker's own native/raw scraped currency (as recorded in
# yahoo_targets_*.txt) — NOT converted to USD. This deliberately matches eToro's own
# Low/Avg/High, which are also stored in native currency and were never converted;
# converting only Yahoo's numbers here previously produced nonsense Upside% math when
# compared against a same-currency price/eToro-target pair for non-US exchanges (found
# 2026-08-30 testing Tokyo). `data-yh-currency` is written per row so the UI can label
# the value instead of silently mixing currencies.

def load_yahoo_targets():
    targets = {}
    files = sorted(glob.glob("yahoo_targets_*.txt"))
    for path in files:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line.strip():
                    continue
                parts = line.split('\t')
                while len(parts) < 5:
                    parts.append('')
                ticker, low, avg, high, currency = parts[:5]
                def fmt(v):
                    if not v:
                        return ''
                    try:
                        return f"{float(v.replace(',', '')):.4f}"
                    except ValueError:
                        return ''
                targets[ticker] = {
                    'low': fmt(low),
                    'avg': fmt(avg),
                    'high': fmt(high),
                    'currency': currency,
                }
    return targets

def esc(s):
    return (s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;'))

def main():
    targets = load_yahoo_targets()
    with open(ROWS_FILE, encoding='utf-8') as f:
        html = f.read()

    matched = 0
    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-yh-[a-z]+="[^"]*"', '', tr_open)
        t = targets.get(ticker)
        if not t:
            return tr_open
        matched += 1
        attrs = (
            f' data-yh-low="{esc(t["low"])}"'
            f' data-yh-avg="{esc(t["avg"])}"'
            f' data-yh-high="{esc(t["high"])}"'
            f' data-yh-currency="{esc(t["currency"])}"'
        )
        return tr_open[:-1] + attrs + '>'

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    with open(ROWS_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Yahoo Finance targets merged: {matched} rows tagged (out of {len(targets)} scraped tickers).")

if __name__ == '__main__':
    main()
