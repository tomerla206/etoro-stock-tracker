"""One-time migration: insert new <td> placeholders at the end of every row
in all_rows.html. Idempotent - skips if already migrated. Mirrors
add_insider_column.py's approach exactly.

(This script has been reused/extended each time a new fundamentals column was
added - score-cell, short/rsi/pe, market cap, hedge fund activity, beta,
volume spike, peg/52-week range, secondary-score, risk-score, overallscore,
percentile-cell, roe/instown/currentratio, now quick ratio/ROA/held-insiders
(Score) + gross margin/operating margin/FCF yield/analyst coverage/forward P-E
(Secondary Score) - rather than writing a fresh near-identical migration
script every time.)"""

import re

with open("all_rows.html", "r", encoding="utf-8") as f:
    content = f.read()

new_suffix_marker = re.compile(r'(<td class="currentratio-cell col-currentratio[^"]*"[^>]*>[\s\S]*?</td>)(</tr>)')

if "quickratio-cell" in content:
    print("Already migrated, skipping.")
else:
    count = len(new_suffix_marker.findall(content))
    content = new_suffix_marker.sub(
        r'\1<td class="quickratio-cell col-quickratio empty">&ndash;</td>'
        r'<td class="roa-cell col-roa empty">&ndash;</td>'
        r'<td class="heldinsiders-cell col-heldinsiders empty">&ndash;</td>'
        r'<td class="grossmargin-cell col-grossmargin empty">&ndash;</td>'
        r'<td class="opmargin-cell col-opmargin empty">&ndash;</td>'
        r'<td class="fcfyield-cell col-fcfyield empty">&ndash;</td>'
        r'<td class="coverage-cell col-coverage empty">&ndash;</td>'
        r'<td class="fwdpe-cell col-fwdpe empty">&ndash;</td>\2',
        content,
    )
    with open("all_rows.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Inserted quickratio/roa/heldinsiders/grossmargin/opmargin/fcfyield/coverage/fwdpe cells into {count} rows")
