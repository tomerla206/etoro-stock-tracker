import re

ROWS_FILE = "all_rows.html"


def load_consensus():
    data = {}
    try:
        with open("consensus_ratings.txt", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 3:
                    continue
                ticker, cons, rating = parts
                data[ticker] = (cons, rating)
    except FileNotFoundError:
        pass
    return data


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


RATING_CLASS = {
    "Strong Buy": "rating-buy", "Moderate Buy": "rating-buy",
    "Hold": "rating-hold",
    "Moderate Sell": "rating-sell", "Strong Sell": "rating-sell",
}


def main():
    data = load_consensus()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-cons="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-rating="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        cons, rating = d
        matched += 1
        attrs = f' data-cons="{esc(cons)}" data-rating="{esc(rating)}"'
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    # Also refresh the visible <td> cells for cons/rating (unlike the other
    # merge scripts, these two columns are rendered server-side into all_rows.html
    # directly, not computed client-side from data-* attributes in part3.html).
    def repl_cells(m):
        ticker = m.group(1)
        full_tr = m.group(0)
        d = data.get(ticker)
        if not d:
            return full_tr
        cons, rating = d
        rating_class = RATING_CLASS.get(rating, "")
        full_tr = re.sub(
            r'(<td class="cons-cell col-cons"[^>]*>)[^<]*(</td>)',
            lambda mm: f'{mm.group(1)}{esc(cons)}%{mm.group(2)}',
            full_tr, count=1,
        )
        full_tr = re.sub(
            r'<td class="rating-cell col-rating[^"]*"[^>]*>[^<]*</td>',
            f'<td class="rating-cell col-rating {rating_class}">{esc(rating)}</td>',
            full_tr, count=1,
        )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Consensus/Rating merged: {matched} rows tagged (out of {len(data)} scraped tickers).")


if __name__ == "__main__":
    main()
