import re

ROWS_FILE = "all_rows.html"


def main():
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    # idempotent: strip any previously-injected yh-div cell first
    html = re.sub(
        r'<td class="yh-div col-yahoo[^"]*">[^<]*</td>',
        "",
        html,
    )

    new_cell = '<td class="yh-div col-yahoo empty">&ndash;</td>'

    # insert right after the yh-high cell, before the yh-pct (upside %) cell
    pattern = re.compile(
        r'(<td class="analysis-cell yh-high col-yahoo[^"]*">[^<]*</td>)'
    )
    html, n = pattern.subn(lambda m: m.group(1) + new_cell, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Yahoo dividend placeholder column added to {n} rows.")


if __name__ == "__main__":
    main()
