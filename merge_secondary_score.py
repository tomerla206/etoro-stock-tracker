import re

ROWS_FILE = "all_rows.html"


def load_secondary_score():
    data = {}
    try:
        with open("secondary_score.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 9:
                    continue
                ticker, total, pe_pts, hf_pts, vol_pts, eps_trend_pts, margin_pts, growth_pts, confidence = parts
                data[ticker] = {
                    "total": total, "pe_pts": pe_pts, "hf_pts": hf_pts,
                    "vol_pts": vol_pts, "eps_trend_pts": eps_trend_pts,
                    "margin_pts": margin_pts, "growth_pts": growth_pts, "confidence": confidence,
                }
    except FileNotFoundError:
        pass
    return data


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def score_class(total):
    v = float(total)
    if v >= 7:
        return "score-high"
    if v >= 4:
        return "score-mid"
    return "score-low"


def confidence_class(confidence):
    v = int(confidence)
    if v >= 5:
        return "conf-high"
    if v >= 3:
        return "conf-mid"
    return "conf-low"


def main():
    data = load_secondary_score()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-secscore(?:-[a-z]+)?="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        attrs = (
            f' data-secscore="{esc(d["total"])}"'
            f' data-secscore-pe="{esc(d["pe_pts"])}"'
            f' data-secscore-hf="{esc(d["hf_pts"])}"'
            f' data-secscore-vol="{esc(d["vol_pts"])}"'
            f' data-secscore-epstrend="{esc(d["eps_trend_pts"])}"'
            f' data-secscore-margin="{esc(d["margin_pts"])}"'
            f' data-secscore-growth="{esc(d["growth_pts"])}"'
            f' data-secscore-confidence="{esc(d["confidence"])}"'
        )
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    def repl_cells(m):
        ticker = m.group(1)
        full_tr = m.group(0)
        d = data.get(ticker)
        if not d:
            return full_tr
        cls = score_class(d["total"])
        conf_cls = confidence_class(d["confidence"])
        cell_html = (
            f'{esc(d["total"])}'
            f'<sup class="score-conf {conf_cls}" title="{d["confidence"]}/6 מדדים עם נתונים אמיתיים">{d["confidence"]}/6</sup>'
        )
        full_tr = re.sub(
            r'<td class="secscore-cell col-secscore[^"]*"[^>]*>[\s\S]*?</td>',
            f'<td class="secscore-cell col-secscore {cls}">{cell_html}</td>',
            full_tr, count=1,
        )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Secondary Score merged: {matched} rows tagged (out of {len(data)} scored tickers).")


if __name__ == "__main__":
    main()
