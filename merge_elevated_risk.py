import re

ROWS_FILE = "all_rows.html"
DATA_FILE = "elevated_risk.tsv"


def load_elevated_risk():
    tickers = set()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            tickers.add(line)
    print(f"Loaded {len(tickers)} elevated-risk tickers from {DATA_FILE}")
    return tickers


def patch_row(line):
    # Only touch the <tr ...> opening tag's own class attribute, never
    # anything inside the row (td/span elements also have class="...").
    m = re.match(r'^(\s*<tr\b[^>]*)>', line)
    if not m:
        raise ValueError(f"Could not parse <tr> opening tag in line: {line!r}")
    tag = m.group(1)
    cm = re.search(r'class="([^"]*)"', tag)
    classes = cm.group(1).split() if cm else []
    if "row-elevated-risk" not in classes:
        classes.append("row-elevated-risk")
    new_class_attr = f'class="{" ".join(classes)}"'
    if cm:
        tag = tag[:cm.start()] + new_class_attr + tag[cm.end():]
    else:
        tag = tag + f' {new_class_attr}'
    return tag + ">" + line[m.end():]


def unpatch_row(line):
    m = re.match(r'^(\s*<tr\b[^>]*)>', line)
    if not m:
        raise ValueError(f"Could not parse <tr> opening tag in line: {line!r}")
    tag = m.group(1)
    cm = re.search(r'class="([^"]*)"', tag)
    if not cm:
        return line
    classes = [c for c in cm.group(1).split() if c != "row-elevated-risk"]
    if classes:
        new_class_attr = f'class="{" ".join(classes)}"'
        tag = tag[:cm.start()] + new_class_attr + tag[cm.end():]
    else:
        tag = tag[:cm.start()].rstrip() + tag[cm.end():]
    return tag + ">" + line[m.end():]


def main():
    elevated = load_elevated_risk()
    with open(ROWS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    ticker_re = re.compile(r'data-ticker="([^"]+)"')
    updated = 0
    matched_tickers = set()
    out_lines = []
    for line in lines:
        m = ticker_re.search(line)
        if m:
            ticker = m.group(1)
            has_class = "row-elevated-risk" in line
            if ticker in elevated:
                if not has_class:
                    line = patch_row(line)
                    updated += 1
                matched_tickers.add(ticker)
            elif has_class:
                # Ticker was previously flagged but no longer is; remove it.
                line = unpatch_row(line)
                updated += 1
        out_lines.append(line)

    unmatched = sorted(elevated - matched_tickers)
    if unmatched:
        print(f"WARNING: {len(unmatched)} elevated-risk tickers had no matching row in {ROWS_FILE}: {unmatched}")

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.writelines(out_lines)
    print(f"Updated {updated} rows in {ROWS_FILE}")


if __name__ == "__main__":
    main()
