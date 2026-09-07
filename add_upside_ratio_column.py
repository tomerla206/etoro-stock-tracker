"""One-time migration: insert the TP/Yahoo upside-ratio <td> placeholder into every
row of all_rows.html, between the TipRanks group's last column (% of Profit) and
Yahoo's first column (Low). Idempotent - skips rows that already have it."""
import re

with open("all_rows.html", "r", encoding="utf-8") as f:
    content = f.read()

marker = '<td class="pl-share-cell col-target empty">&ndash;</td><td class="analysis-cell yh-low'
new_cell = '<td class="pl-share-cell col-target empty">&ndash;</td><td class="ratio-cell col-yahoo empty">&ndash;</td><td class="analysis-cell yh-low'

if 'ratio-cell' in content:
    print("Already migrated, skipping.")
else:
    count = content.count(marker)
    content = content.replace(marker, new_cell)
    with open("all_rows.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Inserted ratio-cell into {count} rows")
