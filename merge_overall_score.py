import re

ROWS_FILE = "all_rows.html"
HISTORY_FILE = "score_history.tsv"
SPARK_POINTS = 14  # last N distinct days shown in the inline sparkline


def load_overall_score():
    data = {}
    try:
        with open("overall_score.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 5:
                    continue
                ticker, total, score_component, secscore_component, confidence = parts
                data[ticker] = {
                    "total": total, "score_component": score_component,
                    "secscore_component": secscore_component, "confidence": confidence,
                }
    except FileNotFoundError:
        pass
    return data


def load_score_change():
    data = {}
    try:
        with open("score_change.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 5:
                    continue
                ticker, delta, direction, prev_date, latest_date = parts
                data[ticker] = {
                    "delta": delta, "direction": direction,
                    "prev_date": prev_date, "latest_date": latest_date,
                }
    except FileNotFoundError:
        pass
    return data


def load_sparkline_history():
    """ticker -> last SPARK_POINTS distinct days' Overall Score, oldest first.
    Reads score_history.tsv directly rather than via a separate script/file -
    this is a display transform of existing history, not a new signal."""
    by_ticker_by_date = {}
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f:
            header_len = None
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if header_len is None:
                    header_len = len(parts)
                if len(parts) != header_len:
                    continue
                date, ticker = parts[0], parts[1]
                overallscore = parts[-2]
                try:
                    value = float(overallscore)
                except ValueError:
                    continue
                by_ticker_by_date.setdefault(ticker, {})[date] = value
    except FileNotFoundError:
        pass

    data = {}
    for ticker, dated_values in by_ticker_by_date.items():
        dates = sorted(dated_values)[-SPARK_POINTS:]
        data[ticker] = [dated_values[d] for d in dates]
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
    # Thresholds scaled to the current max of 25 (Score's 14 + Secondary
    # Score's 11, previously 11+6=17) at the same ~70%/35% cut points.
    v = int(confidence)
    if v >= 18:
        return "conf-high"
    if v >= 9:
        return "conf-mid"
    return "conf-low"


def main():
    data = load_overall_score()
    changes = load_score_change()
    sparklines = load_sparkline_history()

    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-overallscore(?:-[a-z]+)?="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        history = sparklines.get(ticker) or []
        attrs = (
            f' data-overallscore="{esc(d["total"])}"'
            f' data-overallscore-score="{esc(d["score_component"])}"'
            f' data-overallscore-secscore="{esc(d["secscore_component"])}"'
            f' data-overallscore-confidence="{esc(d["confidence"])}"'
            f' data-overallscore-history="{",".join(f"{v:.1f}" for v in history)}"'
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

        change_html = ""
        ch = changes.get(ticker)
        if ch:
            arrow = "▲" if ch["direction"] == "up" else "▼"
            change_cls = "score-change-up" if ch["direction"] == "up" else "score-change-down"
            title = f'שינוי של {ch["delta"]} נק\' מ-{ch["prev_date"]} ל-{ch["latest_date"]}'
            change_html = f'<span class="score-change {change_cls}" title="{title}">{arrow}</span>'

        cell_html = (
            f'{esc(d["total"])}'
            f'<sup class="score-conf {conf_cls}" title="{d["confidence"]}/25 מדדים עם נתונים אמיתיים (משוקלל משני הציונים)">{d["confidence"]}/25</sup>'
            f'{change_html}'
            f'<span class="oscore-spark" aria-hidden="true"></span>'
        )
        full_tr = re.sub(
            r'<td class="overallscore-cell col-overallscore[^"]*"[^>]*>[\s\S]*?</td>',
            f'<td class="overallscore-cell col-overallscore {cls}">{cell_html}</td>',
            full_tr, count=1,
        )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Overall Score merged: {matched} rows tagged (out of {len(data)} scored tickers, "
          f"{len(changes)} with a meaningful change, {len(sparklines)} with history).")


if __name__ == "__main__":
    main()
