"""
Code name: SCAN LOSSES. Builds red_pl_report.html: every HELD position
(Real + Virtual) with P/L below 0%, its entry/current price, analyst
target, dollar loss, and a rough estimated time-to-breakeven based on the
analyst target trajectory.

Reads portfolio_virtual.tsv + portfolio_real.tsv (private, gitignored -
live SCAN HOLDINGS data) and all_rows.html (site's per-ticker analyst/price
data). Only meaningful after a SCAN HOLDINGS pass has refreshed those two
files - this script itself never touches eToro, it just re-renders
whatever is already on disk, which is why it's safe to run on its own
(standalone "SCAN LOSSES"), chained into fundamentals_scan.py's local-only
tail, AND re-run at the end of every SCAN HOLDINGS pass - all three
triggers just re-derive the same page from the same source files.

A "Buy"-rated ticker whose analyst target is at or below the current price
is treated as broken source data (seen once with ALSEN.PA, where
Low=Avg=High=1.00 exactly - a failed-scrape placeholder, not a real target)
and its target/upside/breakeven columns are blanked out rather than shown
as a nonsensical negative-upside "Buy".

Run: python build_red_pl_report.py
Output: red_pl_report.html
"""

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).parent
PLPCT_THRESHOLD = 0.0
ACCOUNTS = [("Virtual", "portfolio_virtual.tsv"), ("Real", "portfolio_real.tsv")]

TEMPLATE = r"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>הפסדים בוירטואלי</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f5f3ef;
    --surface: #ffffff;
    --surface-2: #f0ede7;
    --border: #ddd7cc;
    --text: #201d18;
    --text-dim: #6b6459;
    --accent: #b8850f;
    --accent-soft: #f3e6c8;
    --loss-1: #7a8a72;
    --loss-2: #c9a84c;
    --loss-3: #d98a4a;
    --loss-4: #cc5f4a;
    --loss-5: #b03d3d;
    --low-conf: #a8875a;
    --row-hover: #f0ede7;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #171512;
      --surface: #201d18;
      --surface-2: #262219;
      --border: #3a352b;
      --text: #ede8de;
      --text-dim: #9c9587;
      --accent: #e0b04f;
      --accent-soft: #3a2f18;
      --loss-1: #8fa085;
      --loss-2: #d4b25a;
      --loss-3: #e09a5c;
      --loss-4: #dd7a63;
      --loss-5: #d15a5a;
      --low-conf: #c4a06b;
      --row-hover: #262219;
    }
  }
  :root[data-theme="dark"] {
    --bg: #171512;
    --surface: #201d18;
    --surface-2: #262219;
    --border: #3a352b;
    --text: #ede8de;
    --text-dim: #9c9587;
    --accent: #e0b04f;
    --accent-soft: #3a2f18;
    --loss-1: #8fa085;
    --loss-2: #d4b25a;
    --loss-3: #e09a5c;
    --loss-4: #dd7a63;
    --loss-5: #d15a5a;
    --low-conf: #c4a06b;
    --row-hover: #262219;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: 'Heebo', system-ui, sans-serif;
    direction: rtl;
    padding: 28px 20px 60px;
  }
  .wrap { max-width: 1180px; margin: 0 auto; }
  .masthead {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 6px;
  }
  h1 {
    font-size: clamp(24px, 4vw, 32px);
    font-weight: 800;
    margin: 0;
    text-wrap: balance;
    letter-spacing: -0.01em;
  }
  .meta {
    color: var(--text-dim);
    font-size: 13px;
    font-family: 'IBM Plex Mono', monospace;
  }
  .subtitle {
    color: var(--text-dim);
    font-size: 15px;
    margin: 6px 0 22px;
    max-width: 62ch;
  }
  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
  }
  .stat {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
  }
  .stat .label {
    font-size: 12px;
    color: var(--text-dim);
    margin-bottom: 6px;
  }
  .stat .value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 22px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
  }
  .stat.warn .value { color: var(--loss-5); }

  .disclaimer {
    background: var(--accent-soft);
    border: 1px solid var(--accent);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13.5px;
    line-height: 1.65;
    margin-bottom: 24px;
    color: var(--text);
  }
  .disclaimer strong { display: block; margin-bottom: 4px; }

  .table-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow-x: auto;
  }
  table { width: 100%; border-collapse: collapse; font-size: 13.5px; min-width: 920px; }
  thead th {
    position: sticky;
    top: 0;
    background: var(--surface-2);
    text-align: right;
    padding: 11px 12px;
    font-weight: 600;
    color: var(--text-dim);
    white-space: nowrap;
    cursor: pointer;
    user-select: none;
    border-bottom: 1px solid var(--border);
  }
  thead th:hover { color: var(--text); }
  thead th .arrow { font-size: 9px; margin-inline-start: 4px; opacity: 0.7; }
  tbody td {
    padding: 9px 12px;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
    font-family: 'IBM Plex Mono', monospace;
    font-variant-numeric: tabular-nums;
  }
  tbody td.name-cell { font-family: 'Heebo', system-ui, sans-serif; white-space: normal; }
  tbody tr:last-child td { border-bottom: none; }
  tbody tr:hover td { background: var(--row-hover); }
  .ticker-link { color: var(--text); text-decoration: none; font-weight: 700; }
  .ticker-link:hover { text-decoration: underline; }
  .company { color: var(--text-dim); font-size: 12px; display: block; }
  .plpct-bar {
    display: inline-block;
    min-width: 58px;
    text-align: left;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    color: #1a1508;
  }
  .low-conf { color: var(--low-conf); font-size: 11px; font-family: 'Heebo', sans-serif; }
  .note { color: var(--text-dim); font-size: 12px; font-family: 'Heebo', sans-serif; }
  .rating {
    font-family: 'Heebo', sans-serif;
    font-size: 11.5px;
    color: var(--text-dim);
  }
  .acct-badge {
    font-family: 'Heebo', sans-serif;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid var(--border);
  }
  .acct-real { color: var(--loss-5); border-color: var(--loss-5); }
  .acct-virtual { color: var(--text-dim); }
  footer {
    margin-top: 22px;
    font-size: 12px;
    color: var(--text-dim);
    text-align: center;
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="masthead">
    <h1>הפוזיציות בהפסד — Real + Virtual</h1>
    <div class="meta" id="genDate">__GEN_DATE__</div>
  </div>
  <p class="subtitle">כל ההחזקות בשני החשבונות (Real + Virtual) עם P/L מתחת ל-0%‎, ממוינות מהגרוע לקל ביותר. לכל שורה: מחיר כניסה, מחיר נוכחי, יעד אנליסטים ממוצע, ואומדן זמן משוער לחזרה לאיזון.</p>

  <div class="stats">
    <div class="stat warn">
      <div class="label">מניות באדום</div>
      <div class="value" id="statCount">—</div>
    </div>
    <div class="stat warn">
      <div class="label">הפסד לא ממומש (משוער)</div>
      <div class="value" id="statLoss">—</div>
    </div>
    <div class="stat">
      <div class="label">P/L ממוצע</div>
      <div class="value" id="statAvg">—</div>
    </div>
    <div class="stat">
      <div class="label">סה"כ מושקע בפוזיציות אלה</div>
      <div class="value" id="statInvested">—</div>
    </div>
  </div>

  <div class="disclaimer">
    <strong>איך לקרוא את "אומדן זמן לאיזון" — ולמה להיזהר ממנו</strong>
    האומדן מניח שהמחיר "יטפס" בקצב קבוע לכיוון יעד המחיר הממוצע של האנליסטים (טווח של כ־12 חודש), ומחשב כמה זמן ייקח לחזור למחיר הכניסה שלך לפי אותו קצב. זו הערכה גסה בלבד — לא תחזית מבוססת, ולא המלצת השקעה. במניות עם כיסוי אנליסטים דל (1-2 אנליסטים בלבד, מסומן ⚠) היעד עצמו לא אמין, והאומדן יכול לצאת קיצוני או חסר משמעות. מחיר "נוכחי" מבוסס על הסריקה היומית האחרונה ולא בזמן אמת. שורה עם דירוג "Buy" אבל יעד מתחת למחיר הנוכחי מסומנת כנתון שבור במקור (⚠ נתון יעד שבור) ומוצגת בלי יעד/Upside/זמן איזון, במקום Upside שלילי חסר היגיון.
  </div>

  <div class="table-wrap">
    <table id="tbl">
      <thead>
        <tr>
          <th data-col="0" data-type="text">טיקר / חברה<span class="arrow"></span></th>
          <th data-col="1" data-type="text">חשבון<span class="arrow"></span></th>
          <th data-col="2" data-type="num">מחיר כניסה<span class="arrow"></span></th>
          <th data-col="3" data-type="num">מחיר נוכחי<span class="arrow"></span></th>
          <th data-col="4" data-type="num">P/L%<span class="arrow"></span></th>
          <th data-col="5" data-type="num">הפסד בדולרים<span class="arrow"></span></th>
          <th data-col="6" data-type="num">הושקע<span class="arrow"></span></th>
          <th data-col="7" data-type="num">יעד אנליסטים<span class="arrow"></span></th>
          <th data-col="8" data-type="num">Upside ליעד<span class="arrow"></span></th>
          <th data-col="9" data-type="text">דירוג<span class="arrow"></span></th>
          <th data-col="10" data-type="num">זמן משוער לאיזון<span class="arrow"></span></th>
        </tr>
      </thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>

  <footer>נוצר אוטומטית מתוך portfolio_virtual.tsv + all_rows.html · אינו מהווה ייעוץ השקעות</footer>
</div>

<script>
const DATA = __DATA_JSON__;

const CCY_SYM = { USD: '$', EUR: '€', GBX: '£', GBP: '£' };
function fmtPrice(v, ccy) {
  if (v === null || v === undefined) return '—';
  const sym = CCY_SYM[ccy] || '';
  const dec = v < 5 ? 4 : v < 100 ? 2 : 2;
  return sym + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: dec });
}
function plColor(pct) {
  if (pct <= -30) return 'var(--loss-5)';
  if (pct <= -15) return 'var(--loss-4)';
  if (pct <= -8) return 'var(--loss-3)';
  if (pct <= -4) return 'var(--loss-2)';
  return 'var(--loss-1)';
}
function fmtMonths(m, note) {
  if (note === 'Already at/above entry') return '<span class="note">המחיר כבר מעל הכניסה (לפי הסריקה)</span>';
  if (note === 'No live price') return '<span class="note">אין מחיר חי</span>';
  if (note && note.startsWith('Analyst target data broken')) return '<span class="note">⚠ נתון יעד שבור במקור</span>';
  if (note) return '<span class="note">היעד מתחת למחיר הנוכחי</span>';
  if (m === null || m === undefined) return '<span class="note">—</span>';
  if (m < 1) return `~${Math.round(m * 30)} ימים`;
  return `~${m.toFixed(1)} חודשים`;
}

function invested(d) {
  return d.netvalue / (1 + d.plpct / 100);
}
function lossDollars(d) {
  return d.netvalue - invested(d);
}

function render(rows) {
  const tbody = document.getElementById('tbody');
  tbody.innerHTML = rows.map(d => {
    const lowConf = (!d.coverage || parseInt(d.coverage, 10) <= 2);
    const inv = invested(d);
    const loss = lossDollars(d);
    return `<tr>
      <td class="name-cell">
        <a class="ticker-link" href="https://www.etoro.com/markets/${d.ticker.toLowerCase()}/research" target="_blank" rel="noopener">${d.ticker}</a>
        <span class="company">${d.name}</span>
      </td>
      <td data-raw="${d.account}"><span class="acct-badge ${d.account === 'Real' ? 'acct-real' : 'acct-virtual'}">${d.account === 'Real' ? 'אמיתי' : 'וירטואלי'}</span></td>
      <td data-raw="${d.entry}">${fmtPrice(d.entry, d.currency)}</td>
      <td data-raw="${d.price ?? ''}">${fmtPrice(d.price, d.currency)}</td>
      <td data-raw="${d.plpct}"><span class="plpct-bar" style="background:${plColor(d.plpct)}">${d.plpct.toFixed(1)}%</span></td>
      <td data-raw="${loss}" style="color:var(--loss-5);font-weight:600;">-$${Math.round(Math.abs(loss)).toLocaleString('en-US')}</td>
      <td data-raw="${inv}">$${Math.round(inv).toLocaleString('en-US')}</td>
      <td data-raw="${d.target ?? ''}">${fmtPrice(d.target, d.currency)}</td>
      <td data-raw="${d.upside_pct ?? ''}">${d.upside_pct !== null ? (d.upside_pct > 0 ? '+' : '') + d.upside_pct.toFixed(1) + '%' : '—'}${lowConf && d.upside_pct !== null ? ' <span class="low-conf">⚠ כיסוי דל</span>' : ''}</td>
      <td class="rating" data-raw="${d.rating || ''}">${d.rating || '—'}${d.coverage ? ` (${d.coverage})` : ''}</td>
      <td data-raw="${d.months_to_breakeven ?? 999999}">${fmtMonths(d.months_to_breakeven, d.breakeven_note)}</td>
    </tr>`;
  }).join('');
}

render(DATA);

document.getElementById('statCount').textContent = DATA.length;
const totalLoss = DATA.reduce((s, d) => s + lossDollars(d), 0);
document.getElementById('statLoss').textContent = '$' + Math.round(totalLoss).toLocaleString('en-US');
const avgPl = DATA.reduce((s, d) => s + d.plpct, 0) / DATA.length;
document.getElementById('statAvg').textContent = avgPl.toFixed(1) + '%';
const totalInvested = DATA.reduce((s, d) => s + invested(d), 0);
document.getElementById('statInvested').textContent = '$' + Math.round(totalInvested).toLocaleString('en-US');

// Sorting
const table = document.getElementById('tbl');
const headers = table.querySelectorAll('th');
let sortCol = 4, sortDir = 'asc'; // default: P/L% ascending (worst first) — matches initial data order

function applySort(colIdx, type, dir) {
  const rows = Array.from(document.getElementById('tbody').querySelectorAll('tr'));
  rows.sort((a, b) => {
    const ca = a.children[colIdx], cb = b.children[colIdx];
    let cmp;
    if (type === 'num') {
      const na = parseFloat(ca.dataset.raw), nb = parseFloat(cb.dataset.raw);
      cmp = (isNaN(na) ? Infinity : na) - (isNaN(nb) ? Infinity : nb);
    } else {
      cmp = (ca.dataset.raw || ca.textContent).localeCompare(cb.dataset.raw || cb.textContent);
    }
    return dir === 'asc' ? cmp : -cmp;
  });
  const tbody = document.getElementById('tbody');
  rows.forEach(r => tbody.appendChild(r));
  headers.forEach(h => {
    const arrow = h.querySelector('.arrow');
    arrow.innerHTML = parseInt(h.dataset.col, 10) === colIdx ? (dir === 'asc' ? '▲' : '▼') : '';
  });
}

headers.forEach(h => {
  h.addEventListener('click', () => {
    const colIdx = parseInt(h.dataset.col, 10);
    const type = h.dataset.type;
    if (sortCol === colIdx) { sortDir = sortDir === 'asc' ? 'desc' : 'asc'; }
    else { sortCol = colIdx; sortDir = type === 'text' ? 'asc' : 'asc'; }
    applySort(sortCol, type, sortDir);
  });
});

applySort(sortCol, 'num', sortDir);
</script>
</body>
</html>
"""


def load_portfolio(account, filename):
    rows = []
    path = ROOT / filename
    if not path.exists():
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 8:
                continue
            ticker, name, units, avgopen, pl, plpct, netvalue, status = parts[:8]
            if status != "HELD":
                continue
            try:
                plpct_f = float(plpct)
                avgopen_f = float(avgopen)
                netvalue_f = float(netvalue)
            except ValueError:
                continue
            if plpct_f < PLPCT_THRESHOLD:
                rows.append((ticker, {
                    "account": account, "name": name, "avgopen": avgopen_f,
                    "plpct": plpct_f, "netvalue": netvalue_f,
                }))
    return rows


def get_attr(block, attr):
    m = re.search(attr + r'="([^"]*)"', block)
    return m.group(1) if m else ""


def main():
    portfolio = []
    for account, filename in ACCOUNTS:
        portfolio.extend(load_portfolio(account, filename))
    if not portfolio:
        print("No HELD positions below the P/L threshold (or portfolio_virtual.tsv/portfolio_real.tsv missing) - skipping.")
        return

    html = (ROOT / "all_rows.html").read_text(encoding="utf-8")

    results = []
    for ticker, data in portfolio:
        m = re.search(r'<tr data-ticker="' + re.escape(ticker) + r'"[^>]*>', html)
        block = m.group(0) if m else ""
        price = get_attr(block, "data-price")
        avg_target = get_attr(block, "data-avg")
        yh_avg = get_attr(block, "data-yh-avg")
        rating = get_attr(block, "data-rating")
        currency = get_attr(block, "data-currency")
        coverage = get_attr(block, "data-coverage")

        data["price"] = float(price) if price else None
        target_raw = avg_target if avg_target else yh_avg
        data["avg_target"] = float(target_raw) if target_raw else None
        data["rating"] = rating
        data["currency"] = currency
        data["coverage"] = coverage
        results.append((ticker, data))

    out = []
    for ticker, d in results:
        price = d["price"]
        target = d["avg_target"]
        entry = d["avgopen"]
        rating = d["rating"]

        broken_target = (
            target is not None and price and price > 0 and target <= price
            and rating in ("Strong Buy", "Moderate Buy", "Buy")
        )
        if broken_target:
            target = None

        upside_pct = None
        if price and target and price > 0:
            upside_pct = (target - price) / price * 100.0

        months_to_breakeven = None
        breakeven_note = ""
        if broken_target:
            breakeven_note = "Analyst target data broken at source"
        elif not price or price <= 0:
            breakeven_note = "No live price"
        elif entry <= price:
            breakeven_note = "Already at/above entry"
        elif not target or target <= price:
            breakeven_note = "Target at/below current price"
        else:
            annual_r = (target - price) / price
            monthly_r = (1 + annual_r) ** (1 / 12) - 1
            if monthly_r <= 0:
                breakeven_note = "Flat/negative implied growth"
            else:
                months_to_breakeven = round(math.log(entry / price) / math.log(1 + monthly_r), 1)

        out.append({
            "ticker": ticker,
            "account": d["account"],
            "name": d["name"],
            "entry": entry,
            "price": price,
            "plpct": round(d["plpct"], 2),
            "target": target,
            "upside_pct": round(upside_pct, 1) if upside_pct is not None else None,
            "rating": rating,
            "coverage": d.get("coverage", ""),
            "months_to_breakeven": months_to_breakeven,
            "breakeven_note": breakeven_note,
            "currency": d["currency"],
            "netvalue": round(d["netvalue"], 2),
        })

    out.sort(key=lambda r: r["plpct"])

    import datetime
    gen_date = datetime.date.today().strftime("%d/%m/%Y")

    page = TEMPLATE.replace("__DATA_JSON__", json.dumps(out, ensure_ascii=False, indent=2))
    page = page.replace("__GEN_DATE__", gen_date)

    (ROOT / "red_pl_report.html").write_text(page, encoding="utf-8")
    print(f"Wrote red_pl_report.html ({len(out)} positions below {PLPCT_THRESHOLD}% P/L)")


if __name__ == "__main__":
    main()
