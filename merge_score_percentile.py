import re

ROWS_FILE = "all_rows.html"


def load_percentile():
    data = {}
    try:
        with open("score_percentile.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 4:
                    continue
                ticker, percentile, sector, sector_size = parts
                data[ticker] = {"percentile": percentile, "sector": sector, "sector_size": sector_size}
    except FileNotFoundError:
        pass
    return data


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def percentile_class(percentile):
    v = float(percentile)
    if v >= 70:
        return "score-high"
    if v >= 30:
        return "score-mid"
    return "score-low"


def main():
    data = load_percentile()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-percentile(?:-[a-z]+)?="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        attrs = (
            f' data-percentile="{esc(d["percentile"])}"'
            f' data-percentile-sector="{esc(d["sector"])}"'
            f' data-percentile-sectorsize="{esc(d["sector_size"])}"'
        )
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    def repl_cells(m):
        ticker = m.group(1)
        full_tr = m.group(0)
        d = data.get(ticker)
        if not d:
            return full_tr
        cls = percentile_class(d["percentile"])
        title = f'{d["percentile"]}-אחוז בסקטור {esc(d["sector"])} (מתוך {d["sector_size"]} חברות)'
        cell_html = f'<span title="{title}">{esc(d["percentile"])}%</span>'
        full_tr = re.sub(
            r'<td class="percentile-cell col-percentile[^"]*"[^>]*>[\s\S]*?</td>',
            f'<td class="percentile-cell col-percentile {cls}">{cell_html}</td>',
            full_tr, count=1,
        )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Score Percentile merged: {matched} rows tagged (out of {len(data)} ranked tickers).")


if __name__ == "__main__":
    main()
