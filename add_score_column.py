"""One-time migration: insert the ROE/Institutional Ownership/Current Ratio
<td> placeholders at the end of every row in all_rows.html. Idempotent -
skips if already migrated. Mirrors add_insider_column.py's approach exactly.

(This script has been reused/extended each time a new fundamentals column was
added - score-cell, short/rsi/pe, market cap, hedge fund activity, beta,
volume spike, peg/52-week range, secondary-score, risk-score, overallscore,
percentile-cell, now roe/instown/currentratio - rather than writing a fresh
near-identical migration script every time.)"""

import re

with open("all_rows.html", "r", encoding="utf-8") as f:
    content = f.read()

new_suffix_marker = re.compile(r'(<td class="percentile-cell col-percentile[^"]*"[^>]*>[\s\S]*?</td>)(</tr>)')

if "roe-cell" in content:
    print("Already migrated, skipping.")
else:
    count = len(new_suffix_marker.findall(content))
    content = new_suffix_marker.sub(
        r'\1<td class="roe-cell col-roe empty">&ndash;</td>'
        r'<td class="instown-cell col-instown empty">&ndash;</td>'
        r'<td class="currentratio-cell col-currentratio empty">&ndash;</td>\2',
        content,
    )
    with open("all_rows.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Inserted roe/instown/currentratio cells into {count} rows")
