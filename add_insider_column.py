"""One-time migration: append the insider-activity <td> placeholder to the end
of every row in all_rows.html (after the My Portfolio group's last column).
Idempotent - skips if already migrated."""

with open("all_rows.html", "r", encoding="utf-8") as f:
    content = f.read()

marker = '<td class="my-plpct col-target empty">&ndash;</td></tr>'
new_cell = '<td class="my-plpct col-target empty">&ndash;</td><td class="ins-cell col-insider empty">&ndash;</td></tr>'

if "ins-cell" in content:
    print("Already migrated, skipping.")
else:
    count = content.count(marker)
    content = content.replace(marker, new_cell)
    with open("all_rows.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Inserted ins-cell into {count} rows")
