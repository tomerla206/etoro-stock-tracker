import re

ROWS_FILE = "all_rows.html"


def load_hedgefund():
    data = {}
    try:
        with open("hedge_fund_activity.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 5:
                    continue
                ticker, added, reduced, unchanged, total = parts
                data[ticker] = {"added": added, "reduced": reduced, "unchanged": unchanged, "total": total}
    except FileNotFoundError:
        pass
    return data


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def hedgefund_class(added, reduced):
    added, reduced = int(added), int(reduced)
    if added > reduced:
        return "grade-good"
    if reduced > added:
        return "grade-bad"
    return "grade-mid"


def main():
    data = load_hedgefund()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-hf-[a-z]+="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        net = int(d["added"]) - int(d["reduced"])
        attrs = (
            f' data-hf-added="{esc(d["added"])}"'
            f' data-hf-reduced="{esc(d["reduced"])}"'
            f' data-hf-unchanged="{esc(d["unchanged"])}"'
            f' data-hf-total="{esc(d["total"])}"'
            f' data-hf-net="{net}"'
        )
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    def repl_cells(m):
        ticker = m.group(1)
        full_tr = m.group(0)
        d = data.get(ticker)
        if not d:
            return full_tr
        cls = hedgefund_class(d["added"], d["reduced"])
        label = f'{d["added"]}A/{d["reduced"]}R/{d["unchanged"]}N'
        full_tr = re.sub(
            r'<td class="hf-cell col-hf[^"]*"[^>]*>[\s\S]*?</td>',
            f'<td class="hf-cell col-hf {cls}">{esc(label)}</td>',
            full_tr, count=1,
        )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Hedge Fund Activity merged: {matched} rows tagged (out of {len(data)} scraped tickers).")


if __name__ == "__main__":
    main()
