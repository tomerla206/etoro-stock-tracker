import re

ROWS_FILE = "all_rows.html"


def load_growth_score():
    data = {}
    try:
        with open("growth_score.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 6:
                    continue
                ticker, total, quarterly_pts, nextyear_pts, fiveyear_pts, confidence = parts
                data[ticker] = {
                    "total": total, "quarterly_pts": quarterly_pts,
                    "nextyear_pts": nextyear_pts, "fiveyear_pts": fiveyear_pts,
                    "confidence": confidence,
                }
    except FileNotFoundError:
        pass
    return data


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def growth_class(total):
    v = float(total)
    if v >= 7:
        return "score-high"
    if v >= 4:
        return "score-mid"
    return "score-low"


def confidence_class(confidence):
    v = int(confidence)
    if v >= 3:
        return "conf-high"
    if v >= 2:
        return "conf-mid"
    return "conf-low"


def main():
    data = load_growth_score()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-growthscore(?:-[a-z]+)?="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        attrs = (
            f' data-growthscore="{esc(d["total"])}"'
            f' data-growthscore-quarterly="{esc(d["quarterly_pts"])}"'
            f' data-growthscore-nextyear="{esc(d["nextyear_pts"])}"'
            f' data-growthscore-fiveyear="{esc(d["fiveyear_pts"])}"'
            f' data-growthscore-confidence="{esc(d["confidence"])}"'
        )
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    def repl_cells(m):
        ticker = m.group(1)
        full_tr = m.group(0)
        d = data.get(ticker)
        if not d:
            return full_tr
        cls = growth_class(d["total"])
        conf_cls = confidence_class(d["confidence"])
        cell_html = (
            f'{esc(d["total"])}'
            f'<sup class="score-conf {conf_cls}" title="{d["confidence"]}/3 מדדים עם נתונים אמיתיים">{d["confidence"]}/3</sup>'
        )
        full_tr = re.sub(
            r'<td class="growthscore-cell col-growthscore[^"]*"[^>]*>[\s\S]*?</td>',
            f'<td class="growthscore-cell col-growthscore {cls}">{cell_html}</td>',
            full_tr, count=1,
        )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Growth Score merged: {matched} rows tagged (out of {len(data)} scored tickers).")


if __name__ == "__main__":
    main()
