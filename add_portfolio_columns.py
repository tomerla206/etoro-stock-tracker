import re

ROWS_FILE = "all_rows.html"

def main():
    with open(ROWS_FILE, encoding='utf-8') as f:
        html = f.read()

    # idempotent: strip any previously-injected "my portfolio" cells first
    html = re.sub(
        r'<td class="my-units col-target[^"]*">[^<]*</td>'
        r'<td class="my-avgopen col-target[^"]*">[^<]*</td>'
        r'<td class="my-pl col-target[^"]*">[^<]*</td>'
        r'<td class="my-plpct col-target[^"]*">[^<]*</td>',
        '',
        html,
    )

    new_cells = (
        '<td class="my-units col-target empty">&ndash;</td>'
        '<td class="my-avgopen col-target empty">&ndash;</td>'
        '<td class="my-pl col-target empty">&ndash;</td>'
        '<td class="my-plpct col-target empty">&ndash;</td>'
    )

    html = html.replace('</tr>', new_cells + '</tr>')

    with open(ROWS_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"My-portfolio placeholder columns added to {html.count(new_cells)} rows.")

if __name__ == '__main__':
    main()
