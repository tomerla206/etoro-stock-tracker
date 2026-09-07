import re

ROWS_FILE = "all_rows.html"


def load_risk_score():
    data = {}
    try:
        with open("risk_score.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 8:
                    continue
                ticker, total, beta_pts, range_pts, vol_pts, debt_pts, dtc_pts, confidence = parts
                data[ticker] = {
                    "total": total, "beta_pts": beta_pts, "range_pts": range_pts,
                    "vol_pts": vol_pts, "debt_pts": debt_pts, "dtc_pts": dtc_pts,
                    "confidence": confidence,
                }
    except FileNotFoundError:
        pass
    return data


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def risk_class(total):
    """Deliberately NOT green/red (this isn't a good/bad axis) - blue for
    calm, gray for average, orange for wild, so it reads visually distinct
    from the quality-based Score/Secondary Score columns."""
    v = float(total)
    if v >= 7:
        return "risk-high"
    if v >= 4:
        return "risk-mid"
    return "risk-low"


def confidence_class(confidence):
    v = int(confidence)
    if v >= 4:
        return "conf-high"
    if v >= 2:
        return "conf-mid"
    return "conf-low"


def main():
    data = load_risk_score()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-riskscore(?:-[a-z]+)?="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        attrs = (
            f' data-riskscore="{esc(d["total"])}"'
            f' data-riskscore-beta="{esc(d["beta_pts"])}"'
            f' data-riskscore-range="{esc(d["range_pts"])}"'
            f' data-riskscore-vol="{esc(d["vol_pts"])}"'
            f' data-riskscore-debt="{esc(d["debt_pts"])}"'
            f' data-riskscore-dtc="{esc(d["dtc_pts"])}"'
            f' data-riskscore-confidence="{esc(d["confidence"])}"'
        )
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    def repl_cells(m):
        ticker = m.group(1)
        full_tr = m.group(0)
        d = data.get(ticker)
        if not d:
            return full_tr
        cls = risk_class(d["total"])
        conf_cls = confidence_class(d["confidence"])
        cell_html = (
            f'{esc(d["total"])}'
            f'<sup class="score-conf {conf_cls}" title="{d["confidence"]}/5 מדדים עם נתונים אמיתיים">{d["confidence"]}/5</sup>'
        )
        full_tr = re.sub(
            r'<td class="riskscore-cell col-riskscore[^"]*"[^>]*>[\s\S]*?</td>',
            f'<td class="riskscore-cell col-riskscore {cls}">{cell_html}</td>',
            full_tr, count=1,
        )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Risk Score merged: {matched} rows tagged (out of {len(data)} scored tickers).")


if __name__ == "__main__":
    main()
