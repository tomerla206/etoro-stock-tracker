import re

ROWS_FILE = "all_rows.html"


def load_score():
    data = {}
    try:
        with open("score.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 18:
                    continue
                (ticker, total, rating, upside, insider, short, tech, dispersion, surprise,
                 rating_trend, roe, inst_own, current_ratio, quick_ratio, roa, held_insiders,
                 relative_strength, confidence) = parts
                data[ticker] = {
                    "total": total, "rating": rating, "upside": upside,
                    "insider": insider, "short": short, "tech": tech,
                    "dispersion": dispersion, "surprise": surprise, "rating_trend": rating_trend,
                    "roe": roe, "inst_own": inst_own, "current_ratio": current_ratio,
                    "quick_ratio": quick_ratio, "roa": roa, "held_insiders": held_insiders,
                    "relative_strength": relative_strength, "confidence": confidence,
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
    # Thresholds scaled to the current 15-signal max (previously 14, 11...)
    # at the same ~73%/45% cut points, so a ticker with the same proportion
    # of real vs. defaulted signals keeps the same color as Score grows.
    v = int(confidence)
    if v >= 11:
        return "conf-high"
    if v >= 6:
        return "conf-mid"
    return "conf-low"


def main():
    data = load_score()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-score(?:-[a-z]+)?="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        attrs = (
            f' data-score="{esc(d["total"])}"'
            f' data-score-rating="{esc(d["rating"])}"'
            f' data-score-upside="{esc(d["upside"])}"'
            f' data-score-insider="{esc(d["insider"])}"'
            f' data-score-short="{esc(d["short"])}"'
            f' data-score-tech="{esc(d["tech"])}"'
            f' data-score-dispersion="{esc(d["dispersion"])}"'
            f' data-score-surprise="{esc(d["surprise"])}"'
            f' data-score-ratingtrend="{esc(d["rating_trend"])}"'
            f' data-score-roe="{esc(d["roe"])}"'
            f' data-score-instown="{esc(d["inst_own"])}"'
            f' data-score-currentratio="{esc(d["current_ratio"])}"'
            f' data-score-quickratio="{esc(d["quick_ratio"])}"'
            f' data-score-roa="{esc(d["roa"])}"'
            f' data-score-heldinsiders="{esc(d["held_insiders"])}"'
            f' data-score-relstrength="{esc(d["relative_strength"])}"'
            f' data-score-confidence="{esc(d["confidence"])}"'
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
            f'<sup class="score-conf {conf_cls}" title="{d["confidence"]}/15 מדדים עם נתונים אמיתיים">{d["confidence"]}/15</sup>'
        )
        # non-greedy [\s\S]*? (not [^<]*) so a re-run can match its own
        # previously-inserted <sup> markup instead of only ever matching once
        full_tr = re.sub(
            r'<td class="score-cell col-score[^"]*"[^>]*>[\s\S]*?</td>',
            f'<td class="score-cell col-score {cls}">{cell_html}</td>',
            full_tr, count=1,
        )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Score merged: {matched} rows tagged (out of {len(data)} scored tickers).")


if __name__ == "__main__":
    main()
