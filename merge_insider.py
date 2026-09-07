import re

ROWS_FILE = "all_rows.html"


def load_insider():
    data = {}
    try:
        with open("insider_activity.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 6:
                    continue
                ticker, net, buy, sell, buy_count, sell_count = parts
                data[ticker] = {
                    "net": net, "buy": buy, "sell": sell,
                    "buy_count": buy_count, "sell_count": sell_count,
                }
    except FileNotFoundError:
        pass
    return data


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    data = load_insider()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-ins-[a-z]+="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        attrs = (
            f' data-ins-net="{esc(d["net"])}"'
            f' data-ins-buy="{esc(d["buy"])}"'
            f' data-ins-sell="{esc(d["sell"])}"'
            f' data-ins-buycount="{esc(d["buy_count"])}"'
            f' data-ins-sellcount="{esc(d["sell_count"])}"'
        )
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Insider activity merged: {matched} rows tagged (out of {len(data)} scraped tickers).")


if __name__ == "__main__":
    main()
