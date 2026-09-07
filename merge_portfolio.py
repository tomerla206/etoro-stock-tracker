import re

ROWS_FILE = "all_rows.html"

ACCOUNTS = [
    ("v", "portfolio_virtual.tsv", "portfolio_tp.tsv"),
    ("r", "portfolio_real.tsv", "portfolio_real_tp.tsv"),
]

def load_portfolio(path):
    holdings = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip():
                continue
            parts = line.split('\t')
            while len(parts) < 8:
                parts.append('')
            ticker, company, units, avgopen, pl, plpct, netvalue, status = parts[:8]
            holdings[ticker] = {
                'company': company,
                'units': units,
                'avgopen': avgopen,
                'pl': pl,
                'plpct': plpct,
                'netvalue': netvalue,
                'status': status,
            }
    return holdings

def load_tp(path):
    tp = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip():
                continue
            parts = line.split('\t')
            ticker = parts[0]
            value = parts[1] if len(parts) > 1 else ''
            tp[ticker] = value
    return tp

def esc(s):
    return (s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;'))

def main():
    accounts_data = []
    for prefix, portfolio_file, tp_file in ACCOUNTS:
        holdings = load_portfolio(portfolio_file)
        tp_data = load_tp(tp_file)
        accounts_data.append((prefix, holdings, tp_data))

    with open(ROWS_FILE, encoding='utf-8') as f:
        html = f.read()

    matched_counts = {prefix: 0 for prefix, _, _ in ACCOUNTS}
    tp_counts = {prefix: 0 for prefix, _, _ in ACCOUNTS}

    def repl_tr(m):
        ticker = m.group(1)
        tr_open = m.group(0)
        # strip any previously-injected portfolio attrs (idempotent re-run;
        # also cleans up old single-segment attrs from before per-account support)
        tr_open = re.sub(r'\s*data-pf-[a-z]+(?:-[a-z]+)?="[^"]*"', '', tr_open)
        attrs = ''
        for prefix, holdings, tp_data in accounts_data:
            h = holdings.get(ticker)
            if not h:
                continue
            matched_counts[prefix] += 1
            tp_val = tp_data.get(ticker, '')
            if tp_val:
                tp_counts[prefix] += 1
            attrs += (
                f' data-pf-{prefix}-status="{esc(h["status"])}"'
                f' data-pf-{prefix}-units="{esc(h["units"])}"'
                f' data-pf-{prefix}-avg="{esc(h["avgopen"])}"'
                f' data-pf-{prefix}-pl="{esc(h["pl"])}"'
                f' data-pf-{prefix}-plpct="{esc(h["plpct"])}"'
                f' data-pf-{prefix}-netvalue="{esc(h["netvalue"])}"'
                f' data-pf-{prefix}-tp="{esc(tp_val)}"'
            )
        if not attrs:
            return tr_open
        return tr_open[:-1] + attrs + '>'

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    # Insert badge spans right after the ticker span, one pf-badge per account
    # that holds this ticker, plus one tp-badge per account with known TP.
    def repl_row_for_badge(m):
        full = m.group(0)
        # strip any previously-injected badge spans (idempotent re-run;
        # also cleans up old badges from before per-account support, which
        # had no data-acct attribute at all)
        full = re.sub(r'<span class="pf-badge[^"]*"(?: data-acct="[a-z]")?></span>', '', full)
        full = re.sub(r'<span class="tp-badge[^"]*"(?: data-acct="[a-z]")?></span>', '', full)
        badges = ''
        for prefix, _, _ in ACCOUNTS:
            status_m = re.search(rf'data-pf-{prefix}-status="([^"]*)"', full)
            status = status_m.group(1) if status_m else ''
            if status in ('HELD', 'PENDING'):
                badge_class = 'pf-badge pf-held' if status == 'HELD' else 'pf-badge pf-pending'
                badges += f'<span class="{badge_class}" data-acct="{prefix}"></span>'
                # Show the TP badge for every held/pending position, not just ones
                # that already have a TP — the "no TP set yet" case is exactly
                # when a reminder + a link to go set one is most useful.
                badges += f'<span class="tp-badge" data-acct="{prefix}"></span>'
        if not badges:
            return full
        return full.replace('</span><span class="name">', f'</span>{badges}<span class="name">', 1)

    html = re.sub(r'<tr data-ticker="[^"]+"[^>]*>.*?</tr>', repl_row_for_badge, html, flags=re.DOTALL)

    with open(ROWS_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    for prefix, _, _ in ACCOUNTS:
        label = 'Virtual' if prefix == 'v' else 'Real'
        print(f"{label}: {matched_counts[prefix]} rows tagged, TP known for {tp_counts[prefix]}.")

if __name__ == '__main__':
    main()
