import re
import glob

ROWS_FILE = "all_rows.html"


def load_yahoo_dividends():
    targets = {}
    files = glob.glob("yahoo_dividends_*.txt")
    for path in files:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) < 2:
                    continue
                ticker, div = parts[0], parts[1]
                targets[ticker] = div
    return targets


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    targets = load_yahoo_dividends()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-yh-div="[^"]*"', "", tr_open)
        div = targets.get(ticker)
        if not div:
            return tr_open
        matched += 1
        attrs = f' data-yh-div="{esc(div)}"'
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Yahoo dividends merged: {matched} rows tagged (out of {len(targets)} scraped tickers).")


if __name__ == "__main__":
    main()
