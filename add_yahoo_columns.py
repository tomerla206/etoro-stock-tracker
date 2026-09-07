import re

ROWS_FILE = "all_rows.html"

def main():
    with open(ROWS_FILE, encoding='utf-8') as f:
        html = f.read()

    # idempotent: strip any previously-injected yahoo cells first, wherever they landed
    html = re.sub(
        r'<td class="analysis-cell yh-low col-yahoo[^"]*">[^<]*</td>'
        r'<td class="analysis-cell yh-avg col-yahoo[^"]*">[^<]*</td>'
        r'<td class="analysis-cell yh-high col-yahoo[^"]*">[^<]*</td>',
        '',
        html,
    )
    html = re.sub(
        r'<td class="yh-pct col-yahoo[^"]*">[^<]*</td>'
        r'<td class="yh-alloc col-yahoo[^"]*">[^<]*</td>'
        r'<td class="yh-pl col-yahoo[^"]*">[^<]*</td>'
        r'<td class="yh-plshare col-yahoo[^"]*">[^<]*</td>',
        '',
        html,
    )

    new_cells = (
        '<td class="analysis-cell yh-low col-yahoo empty">&ndash;</td>'
        '<td class="analysis-cell yh-avg col-yahoo empty">&ndash;</td>'
        '<td class="analysis-cell yh-high col-yahoo empty">&ndash;</td>'
        '<td class="yh-pct col-yahoo empty">&ndash;</td>'
        '<td class="yh-alloc col-yahoo empty">&ndash;</td>'
        '<td class="yh-pl col-yahoo empty">&ndash;</td>'
        '<td class="yh-plshare col-yahoo empty">&ndash;</td>'
    )

    # insert right after eToro's own "% of Profit" cell (pl-share-cell), i.e. right
    # before My Portfolio's cells — so the full Yahoo block sits after the full eToro block
    pattern = re.compile(r'(<td class="pl-share-cell col-target[^"]*">[^<]*</td>)')
    html, n = pattern.subn(lambda m: m.group(1) + new_cells, html)

    with open(ROWS_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Yahoo placeholder columns added to {n} rows.")

if __name__ == '__main__':
    main()
