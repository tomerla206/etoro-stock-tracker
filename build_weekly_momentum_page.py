"""
BUILD WEEKLY MOMENTUM PAGE - injects weekly_momentum_score.tsv's rows into
weekly_momentum_template.html, producing the final static weekly_momentum.html
page - same pattern as build_site.py assembling nasdaq-stocks.html from
part1_fixed.html + all_rows.html + part3.html, but for this separate,
standalone page (never merged into the main site's own build).

Run: python build_weekly_momentum_page.py (after compute_weekly_momentum.py
has produced a fresh weekly_momentum_score.tsv)
Result: weekly_momentum.html
"""

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
SCORE_FILE = ROOT / "weekly_momentum_score.tsv"
TEMPLATE_FILE = ROOT / "weekly_momentum_template.html"
OUTPUT_FILE = ROOT / "weekly_momentum.html"


def fmt_num(v, suffix=""):
    if v is None or v == "None" or v == "":
        return '<span class="dim">&ndash;</span>'
    try:
        fv = float(v)
    except (ValueError, TypeError):
        return '<span class="dim">&ndash;</span>'
    return f"{fv:.2f}{suffix}"


def fmt_pct(v):
    if v is None or v == "None" or v == "":
        return '<span class="dim">&ndash;</span>'
    try:
        fv = float(v)
    except (ValueError, TypeError):
        return '<span class="dim">&ndash;</span>'
    cls = "pos" if fv >= 0 else "neg"
    sign = "+" if fv >= 0 else ""
    return f'<span class="{cls}" data-raw="{fv}">{sign}{fv:.1f}%</span>'


def build_row(rank, ticker, score, ret21d, turnover_ratio, range52_pos, turnover_persist,
              rel_strength_10d, rsi2, analyst_revision_pct):
    url = f"https://www.etoro.com/markets/{ticker.lower()}/research"
    return (
        f'<tr>'
        f'<td class="rank-cell">{rank}</td>'
        f'<td><a class="stock-link" href="{url}" target="_blank" rel="noopener">{ticker}</a></td>'
        f'<td class="score-cell">{float(score):.2f}</td>'
        f'<td>{fmt_pct(ret21d)}</td>'
        f'<td>{fmt_num(turnover_ratio, "x")}</td>'
        f'<td>{fmt_num(range52_pos)}</td>'
        f'<td>{fmt_num(turnover_persist, "x")}</td>'
        f'<td>{fmt_pct(rel_strength_10d)}</td>'
        f'<td>{fmt_num(rsi2)}</td>'
        f'<td>{fmt_pct(analyst_revision_pct)}</td>'
        f'</tr>'
    )


def main():
    if not SCORE_FILE.exists():
        print("No weekly_momentum_score.tsv found - run compute_weekly_momentum.py first.")
        return
    if not TEMPLATE_FILE.exists():
        print("Missing weekly_momentum_template.html.")
        return

    rows_html = []
    for line in SCORE_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) != 10:
            continue
        rows_html.append(build_row(*parts))

    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    meta_line = f"נוצר: {generated_at} &middot; {len(rows_html)} מניות (יקום נזיל, מחיר &ge; $5, US) &middot; לחץ על כותרת עמודה למיון"

    template = template.replace("<!--META-->", meta_line)
    template = template.replace("<!--ROWS-->", "\n".join(rows_html))

    OUTPUT_FILE.write_text(template, encoding="utf-8")
    print(f"Built {OUTPUT_FILE.name} with {len(rows_html)} rows")


if __name__ == "__main__":
    main()
