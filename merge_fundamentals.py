import re

ROWS_FILE = "all_rows.html"


def load_fundamentals():
    data = {}
    try:
        with open("fundamentals_data.tsv", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) != 24:
                    continue
                data[parts[0]] = {
                    "short_pct": parts[1], "beta": parts[2], "pe": parts[3], "rsi14": parts[4],
                    "market_cap": parts[8], "market_cap_fmt": parts[9],
                    "volume_ratio": parts[10], "price_change_pct": parts[11],
                    "peg": parts[12], "range52_pos": parts[13],
                    "return_on_equity": parts[21], "current_ratio": parts[22],
                    "institutional_ownership": parts[23],
                }
    except FileNotFoundError:
        pass
    return data


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def fnum(v, decimals=2):
    try:
        return f"{float(v):.{decimals}f}"
    except (ValueError, TypeError):
        return None


def short_class(pct):
    """Same buckets as score_short_interest() in compute_score.py, so the
    color on screen always matches the reasoning behind the Score - low
    Short Interest is bullish (green), high is bearish (red), by degree."""
    v = float(pct)
    if v < 2:
        return "grade-vgood"
    if v < 5:
        return "grade-good"
    if v < 10:
        return "grade-mid"
    if v < 20:
        return "grade-bad"
    return "grade-vbad"


def rsi_class(rsi):
    """Low RSI (oversold) = green (bullish bounce potential), high RSI
    (overbought) = red (pullback risk), graded by degree."""
    v = float(rsi)
    if v <= 20:
        return "grade-vgood"
    if v <= 30:
        return "grade-good"
    if v < 70:
        return "grade-mid"
    if v < 80:
        return "grade-bad"
    return "grade-vbad"


def pe_class(pe):
    """Rough rule-of-thumb only (low P/E = 'cheap', high = 'expensive') -
    unlike Short Interest this is NOT tied to the Score, since P/E is
    deliberately excluded from it (cross-sector comparison is misleading -
    see the column's own tooltip). Negative P/E (a loss-making company)
    is graded neutral since the ratio is meaningless there, not bad."""
    v = float(pe)
    if v < 0:
        return "grade-mid"
    if v < 10:
        return "grade-vgood"
    if v < 15:
        return "grade-good"
    if v < 25:
        return "grade-mid"
    if v < 40:
        return "grade-bad"
    return "grade-vbad"


def peg_class(peg):
    """Same rule-of-thumb shape as pe_class, but on the growth-adjusted PEG
    scale (see the PEG column's own tooltip) - lower is 'cheap relative to
    growth', higher is 'expensive relative to growth'. Not tied to the Score
    (same reasoning as P/E), but IS used by compute_secondary_score.py's
    scoring (preferred over raw P/E there when available)."""
    v = float(peg)
    if v < 0:
        return "grade-mid"
    if v < 1.0:
        return "grade-vgood"
    if v < 1.5:
        return "grade-good"
    if v < 2.5:
        return "grade-mid"
    if v < 4.0:
        return "grade-bad"
    return "grade-vbad"


def roe_class(roe_pct):
    """Same buckets as score_roe() in compute_score.py, so the color always
    matches the Score's own reasoning - higher ROE is graded more bullish."""
    v = float(roe_pct)
    if v > 25:
        return "grade-vgood"
    if v > 15:
        return "grade-good"
    if v > 5:
        return "grade-mid"
    if v > 0:
        return "grade-bad"
    return "grade-vbad"


def inst_own_class(pct):
    """Same buckets as score_institutional_ownership() in compute_score.py -
    higher institutional ownership graded more bullish (more 'smart money'
    confidence), not tied to any objective "correct" level."""
    v = float(pct)
    if v > 70:
        return "grade-vgood"
    if v > 50:
        return "grade-good"
    if v > 30:
        return "grade-mid"
    if v > 10:
        return "grade-bad"
    return "grade-vbad"


def current_ratio_class(ratio):
    """Same SWEET-SPOT shape as score_current_ratio() in compute_score.py -
    unlike the other grades here, higher is not simply better: below 1.0 is
    a liquidity risk (bad), 1.5-3.0 is the healthy range (best), and above
    3.0 circles back to just "mid" (idle cash, not necessarily great)."""
    v = float(ratio)
    if v < 1.0:
        return "grade-vbad"
    if v < 1.5:
        return "grade-mid"
    if v <= 3.0:
        return "grade-vgood"
    return "grade-mid"


def volume_class(ratio, price_change_pct):
    """Unlike Short/RSI/P-E, volume alone has no direction - a spike can
    accompany either a rally or a selloff. Only graded when there's an
    actual spike (ratio >= 2x); direction comes from the same day's price
    move, not the ratio itself."""
    if ratio < 2.0:
        return "grade-mid"
    if price_change_pct is None:
        return "grade-mid"
    if price_change_pct > 1:
        return "grade-vgood" if ratio >= 3.0 else "grade-good"
    if price_change_pct < -1:
        return "grade-vbad" if ratio >= 3.0 else "grade-bad"
    return "grade-mid"


def main():
    data = load_fundamentals()
    with open(ROWS_FILE, encoding="utf-8") as f:
        html = f.read()

    matched = 0

    def repl_tr(m):
        nonlocal matched
        ticker = m.group(1)
        tr_open = m.group(0)
        tr_open = re.sub(r'\s*data-short="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-rsi="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-pe="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-mcap="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-beta="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-vol="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-peg="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-r52="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-roe="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-instown="[^"]*"', "", tr_open)
        tr_open = re.sub(r'\s*data-currentratio="[^"]*"', "", tr_open)
        d = data.get(ticker)
        if not d:
            return tr_open
        matched += 1
        short_pct = fnum(float(d["short_pct"]) * 100, 2) if d["short_pct"] not in (None, "None") else ""
        rsi = fnum(d["rsi14"], 1) if d["rsi14"] not in (None, "None") else ""
        pe = fnum(d["pe"], 1) if d["pe"] not in (None, "None") else ""
        beta = fnum(d["beta"], 2) if d["beta"] not in (None, "None") else ""
        mcap_raw = d["market_cap"] if d["market_cap"] not in (None, "None") else ""
        vol_ratio = fnum(d["volume_ratio"], 2) if d["volume_ratio"] not in (None, "None") else ""
        peg = fnum(d["peg"], 2) if d["peg"] not in (None, "None") else ""
        range52_pos = fnum(d["range52_pos"], 1) if d["range52_pos"] not in (None, "None") else ""
        roe = fnum(float(d["return_on_equity"]) * 100, 1) if d["return_on_equity"] not in (None, "None") else ""
        inst_own = fnum(float(d["institutional_ownership"]) * 100, 1) if d["institutional_ownership"] not in (None, "None") else ""
        current_ratio = fnum(d["current_ratio"], 2) if d["current_ratio"] not in (None, "None") else ""
        attrs = (
            f' data-short="{esc(short_pct)}" data-rsi="{esc(rsi)}" data-pe="{esc(pe)}"'
            f' data-mcap="{esc(mcap_raw)}" data-beta="{esc(beta)}" data-vol="{esc(vol_ratio)}"'
            f' data-peg="{esc(peg)}" data-r52="{esc(range52_pos)}"'
            f' data-roe="{esc(roe)}" data-instown="{esc(inst_own)}" data-currentratio="{esc(current_ratio)}"'
        )
        return tr_open[:-1] + attrs + ">"

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>', repl_tr, html)

    def repl_cells(m):
        ticker = m.group(1)
        full_tr = m.group(0)
        d = data.get(ticker)
        if not d:
            return full_tr

        short_pct = fnum(float(d["short_pct"]) * 100, 2) if d["short_pct"] not in (None, "None") else None
        rsi = fnum(d["rsi14"], 1) if d["rsi14"] not in (None, "None") else None
        pe = fnum(d["pe"], 1) if d["pe"] not in (None, "None") else None

        if short_pct is not None:
            cls = short_class(short_pct)
            full_tr = re.sub(
                r'<td class="short-cell col-short[^"]*"[^>]*>[^<]*</td>',
                f'<td class="short-cell col-short {cls}">{esc(short_pct)}%</td>',
                full_tr, count=1,
            )
        if rsi is not None:
            cls = rsi_class(rsi)
            full_tr = re.sub(
                r'<td class="rsi-cell col-rsi[^"]*"[^>]*>[^<]*</td>',
                f'<td class="rsi-cell col-rsi {cls}">{esc(rsi)}</td>',
                full_tr, count=1,
            )
        if pe is not None:
            cls = pe_class(pe)
            full_tr = re.sub(
                r'<td class="pe-cell col-pe[^"]*"[^>]*>[^<]*</td>',
                f'<td class="pe-cell col-pe {cls}">{esc(pe)}</td>',
                full_tr, count=1,
            )
        mcap = d["market_cap_fmt"] if d["market_cap_fmt"] not in (None, "None", "") else None
        if mcap is not None:
            full_tr = re.sub(
                r'<td class="mcap-cell col-mcap[^"]*"[^>]*>[^<]*</td>',
                f'<td class="mcap-cell col-mcap">{esc(mcap)}</td>',
                full_tr, count=1,
            )
        beta = fnum(d["beta"], 2) if d["beta"] not in (None, "None") else None
        if beta is not None:
            full_tr = re.sub(
                r'<td class="beta-cell col-beta[^"]*"[^>]*>[^<]*</td>',
                f'<td class="beta-cell col-beta">{esc(beta)}</td>',
                full_tr, count=1,
            )
        vol_ratio = fnum(d["volume_ratio"], 2) if d["volume_ratio"] not in (None, "None") else None
        if vol_ratio is not None:
            price_change_pct = None
            try:
                price_change_pct = float(d["price_change_pct"])
            except (ValueError, TypeError):
                pass
            cls = volume_class(float(vol_ratio), price_change_pct)
            full_tr = re.sub(
                r'<td class="vol-cell col-vol[^"]*"[^>]*>[^<]*</td>',
                f'<td class="vol-cell col-vol {cls}">{esc(vol_ratio)}x</td>',
                full_tr, count=1,
            )
        peg = fnum(d["peg"], 2) if d["peg"] not in (None, "None") else None
        if peg is not None:
            cls = peg_class(peg)
            full_tr = re.sub(
                r'<td class="peg-cell col-peg[^"]*"[^>]*>[^<]*</td>',
                f'<td class="peg-cell col-peg {cls}">{esc(peg)}</td>',
                full_tr, count=1,
            )
        range52_pos = fnum(d["range52_pos"], 1) if d["range52_pos"] not in (None, "None") else None
        if range52_pos is not None:
            full_tr = re.sub(
                r'<td class="r52-cell col-r52[^"]*"[^>]*>[^<]*</td>',
                f'<td class="r52-cell col-r52">{esc(range52_pos)}%</td>',
                full_tr, count=1,
            )
        roe = fnum(float(d["return_on_equity"]) * 100, 1) if d["return_on_equity"] not in (None, "None") else None
        if roe is not None:
            cls = roe_class(roe)
            full_tr = re.sub(
                r'<td class="roe-cell col-roe[^"]*"[^>]*>[^<]*</td>',
                f'<td class="roe-cell col-roe {cls}">{esc(roe)}%</td>',
                full_tr, count=1,
            )
        inst_own = fnum(float(d["institutional_ownership"]) * 100, 1) if d["institutional_ownership"] not in (None, "None") else None
        if inst_own is not None:
            cls = inst_own_class(inst_own)
            full_tr = re.sub(
                r'<td class="instown-cell col-instown[^"]*"[^>]*>[^<]*</td>',
                f'<td class="instown-cell col-instown {cls}">{esc(inst_own)}%</td>',
                full_tr, count=1,
            )
        current_ratio = fnum(d["current_ratio"], 2) if d["current_ratio"] not in (None, "None") else None
        if current_ratio is not None:
            cls = current_ratio_class(current_ratio)
            full_tr = re.sub(
                r'<td class="currentratio-cell col-currentratio[^"]*"[^>]*>[^<]*</td>',
                f'<td class="currentratio-cell col-currentratio {cls}">{esc(current_ratio)}</td>',
                full_tr, count=1,
            )
        return full_tr

    html = re.sub(r'<tr data-ticker="([^"]+)"[^>]*>.*?</tr>', repl_cells, html)

    with open(ROWS_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Fundamentals (Short%/RSI/PE/Market Cap/Beta/Volume/PEG/52wRange/ROE/InstOwn/CurrentRatio) merged: {matched} rows tagged (out of {len(data)} scanned tickers).")


if __name__ == "__main__":
    main()
