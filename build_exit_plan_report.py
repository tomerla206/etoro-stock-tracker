"""
Code name: SCAN EXIT PLAN. Builds exit_plan_report.html: for every HELD
Virtual position (regardless of current P/L sign), a suggested exit price
(the eToro Take Profit if the user already set one, otherwise the analyst
average target), the upside from the current price to that goal, and a
rough estimated time to get there - using the same monthly-growth-rate
model as SCAN LOSSES's "time to breakeven" column, generalized to any goal
price instead of just the entry price.

Reads portfolio_virtual.tsv + portfolio_tp.tsv (private, gitignored - live
SCAN HOLDINGS data) and all_rows.html (site's per-ticker analyst/price
data). Never touches eToro itself - just re-renders whatever is already on
disk, so it's safe to run standalone any time those files are refreshed.

Run: python build_exit_plan_report.py
Output: exit_plan_report.html
"""

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).parent

TEMPLATE = r"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>תוכנית יציאה — וירטואלי</title>
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
    --accent: #4c7a5e;
    --accent-soft: #dceadf;
    --gain-1: #4c7a5e;
    --gain-2: #6b9b7a;
    --loss-1: #cc5f4a;
    --low-conf: #a8875a;
    --row-hover: #f0ede7;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #131714;
      --surface: #191d19;
      --surface-2: #202520;
      --border: #333a33;
      --text: #e7ede8;
      --text-dim: #94a096;
      --accent: #6bbf8e;
      --accent-soft: #1d3327;
      --gain-1: #6bbf8e;
      --gain-2: #8fd1a6;
      --loss-1: #dd7a63;
      --low-conf: #c4a06b;
      --row-hover: #202520;
    }
  }
  :root[data-theme="dark"] {
    --bg: #131714;
    --surface: #191d19;
    --surface-2: #202520;
    --border: #333a33;
    --text: #e7ede8;
    --text-dim: #94a096;
    --accent: #6bbf8e;
    --accent-soft: #1d3327;
    --gain-1: #6bbf8e;
    --gain-2: #8fd1a6;
    --loss-1: #dd7a63;
    --low-conf: #c4a06b;
    --row-hover: #202520;
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
  .wrap { max-width: 1220px; margin: 0 auto; }
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
  .header-actions { display: flex; align-items: center; gap: 10px; }
  .back-link {
    color: var(--accent);
    text-decoration: none;
    font-size: 13px;
    font-family: 'Heebo', sans-serif;
    border: 1px solid var(--border);
    padding: 6px 12px;
    border-radius: 999px;
    white-space: nowrap;
  }
  .back-link:hover { background: var(--surface-2); }
  .subtitle {
    color: var(--text-dim);
    font-size: 15px;
    margin: 6px 0 22px;
    max-width: 68ch;
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
  .stat .label { font-size: 12px; color: var(--text-dim); margin-bottom: 6px; }
  .stat .value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 22px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
  }
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
  table { width: 100%; border-collapse: collapse; font-size: 13.5px; min-width: 980px; }
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
  tbody td.rownum { color: var(--text-dim); text-align: center; }
  tbody tr:last-child td { border-bottom: none; }
  tbody tr:hover td { background: var(--row-hover); }
  .ticker-link { color: var(--text); text-decoration: none; font-weight: 700; }
  .ticker-link:hover { text-decoration: underline; }
  .company { color: var(--text-dim); font-size: 12px; display: block; }
  .pill {
    display: inline-block;
    min-width: 58px;
    text-align: left;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    color: #0d1a12;
  }
  .low-conf { color: var(--low-conf); font-size: 11px; font-family: 'Heebo', sans-serif; }
  .note { color: var(--text-dim); font-size: 12px; font-family: 'Heebo', sans-serif; }
  .rating { font-family: 'Heebo', sans-serif; font-size: 11.5px; color: var(--text-dim); }
  .goal-src {
    font-family: 'Heebo', sans-serif;
    font-size: 10.5px;
    font-weight: 600;
    padding: 1px 6px;
    border-radius: 999px;
    border: 1px solid var(--border);
    margin-inline-start: 4px;
  }
  .goal-tp { color: var(--accent); border-color: var(--accent); }
  .goal-target { color: var(--text-dim); }
</style>
</head>
<body>
<div class="wrap">
  <div class="masthead">
    <h1>תוכנית יציאה — וירטואלי</h1>
    <div class="header-actions">
      <div class="meta" id="genDate">__GEN_DATE__</div>
      <a class="back-link" href="nasdaq-stocks.html">&rarr; חזרה לאתר הראשי</a>
    </div>
  </div>
  <p class="subtitle">לכל פוזיציה מוחזקת בוירטואלי: יעד יציאה (ה-Take Profit שקבעת בעטורו אם יש, אחרת יעד האנליסטים הממוצע), ה-Upside מהמחיר הנוכחי אליו, ואומדן זמן משוער להגיע אליו.</p>

  <div class="stats">
    <div class="stat">
      <div class="label">פוזיציות</div>
      <div class="value" id="statCount">—</div>
    </div>
    <div class="stat">
      <div class="label">סה"כ מושקע</div>
      <div class="value" id="statInvested">—</div>
    </div>
    <div class="stat">
      <div class="label">עם TP שהוגדר ידנית</div>
      <div class="value" id="statTP">—</div>
    </div>
    <div class="stat">
      <div class="label">Upside ממוצע ליעד</div>
      <div class="value" id="statUpside">—</div>
    </div>
    <div class="stat">
      <div class="label">רווח פוטנציאלי כולל אם כל היעדים יושגו</div>
      <div class="value" id="statPotential">—</div>
    </div>
  </div>

  <div class="disclaimer">
    <strong>איך לקרוא את זה — ולמה להיזהר</strong>
    "יעד" הוא ה-TP שהגדרת בעטורו אם קיים (מסומן TP), אחרת יעד המחיר הממוצע של אנליסטים (מסומן קונצנזוס). "אומדן זמן" מניח קצב צמיחה חודשי קבוע הנגזר מיעד האנליסטים על פני כ-12 חודש, ומחשב כמה זמן ייקח להגיע ליעד בקצב הזה — הערכה גסה, לא תחזית. במניות עם כיסוי אנליסטים דל (⚠, 1-2 אנליסטים) היעד עצמו פחות אמין. זה כלי לארגון מחשבה, לא ייעוץ השקעות.
  </div>

  <div class="table-wrap">
    <table id="tbl">
      <thead>
        <tr>
          <th data-col="0" data-type="num" class="rownum-th">#<span class="arrow"></span></th>
          <th data-col="1" data-type="text">טיקר / חברה<span class="arrow"></span></th>
          <th data-col="2" data-type="num">מחיר כניסה<span class="arrow"></span></th>
          <th data-col="3" data-type="num">מחיר נוכחי<span class="arrow"></span></th>
          <th data-col="4" data-type="num">P/L% נוכחי<span class="arrow"></span></th>
          <th data-col="5" data-type="num">הושקע<span class="arrow"></span></th>
          <th data-col="6" data-type="num">P/L בדולרים<span class="arrow"></span></th>
          <th data-col="7" data-type="num">שווי נוכחי (הושקע+P/L)<span class="arrow"></span></th>
          <th data-col="8" data-type="num">יעד יציאה<span class="arrow"></span></th>
          <th data-col="9" data-type="num">Upside ליעד<span class="arrow"></span></th>
          <th data-col="10" data-type="num">רווח כולל אם יושג<span class="arrow"></span></th>
          <th data-col="11" data-type="text">דירוג<span class="arrow"></span></th>
          <th data-col="12" data-type="num">זמן משוער ליעד<span class="arrow"></span></th>
        </tr>
      </thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>

  <footer style="margin-top:22px;font-size:12px;color:var(--text-dim);text-align:center;">נוצר אוטומטית מתוך portfolio_virtual.tsv + portfolio_tp.tsv + all_rows.html · אינו מהווה ייעוץ השקעות</footer>
</div>

<script>
const DATA = __DATA_JSON__;

const CCY_SYM = { USD: '$', EUR: '€', GBX: '£', GBP: '£' };
function fmtPrice(v, ccy) {
  if (v === null || v === undefined) return '—';
  const sym = CCY_SYM[ccy] || '';
  const dec = v < 5 ? 4 : 2;
  return sym + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: dec });
}
function plColor(pct) {
  if (pct >= 15) return 'var(--gain-1)';
  if (pct >= 0) return 'var(--gain-2)';
  return 'var(--loss-1)';
}
function fmtMonths(m, note) {
  if (note === 'Already at/above goal') return '<span class="note">היעד כבר הושג לפי הסריקה</span>';
  if (note === 'No live price') return '<span class="note">אין מחיר חי</span>';
  if (note && note.startsWith('broken')) return '<span class="note">⚠ נתון יעד שבור במקור</span>';
  if (note === 'target_horizon') return '<span class="note">יעד קונצנזוס — טווח של כ-12 חודש</span>';
  if (note === 'No goal') return '<span class="note">אין יעד/כיסוי אנליסטים</span>';
  if (m === null || m === undefined) return '<span class="note">—</span>';
  if (m < 1) return `~${Math.round(m * 30)} ימים`;
  return `~${m.toFixed(1)} חודשים`;
}

function fmtUsd(v) {
  if (v === null || v === undefined || isNaN(v)) return '—';
  const sign = v < 0 ? '-' : '';
  return sign + '$' + Math.round(Math.abs(v)).toLocaleString('en-US');
}

function render(rows) {
  const tbody = document.getElementById('tbody');
  tbody.innerHTML = rows.map((d, i) => {
    const lowConf = (!d.coverage || parseInt(d.coverage, 10) <= 2);
    return `<tr>
      <td class="rownum" data-raw="${i + 1}">${i + 1}</td>
      <td class="name-cell">
        <a class="ticker-link" href="https://www.etoro.com/markets/${d.ticker.toLowerCase()}/research" target="_blank" rel="noopener">${d.ticker}</a>
        <span class="company">${d.name}</span>
      </td>
      <td data-raw="${d.entry}">${fmtPrice(d.entry, d.currency)}</td>
      <td data-raw="${d.price ?? ''}">${fmtPrice(d.price, d.currency)}</td>
      <td data-raw="${d.plpct}"><span class="pill" style="background:${plColor(d.plpct)}">${d.plpct.toFixed(1)}%</span></td>
      <td data-raw="${d.invested}">${fmtUsd(d.invested)}</td>
      <td data-raw="${d.pl_dollar}" style="color:${d.pl_dollar < 0 ? 'var(--loss-1)' : 'var(--gain-1)'};font-weight:600;">${fmtUsd(d.pl_dollar)}</td>
      <td data-raw="${d.netvalue}">${fmtUsd(d.netvalue)}</td>
      <td data-raw="${d.goal ?? ''}">${fmtPrice(d.goal, d.currency)}${d.goal !== null ? `<span class="goal-src ${d.goal_source === 'TP' ? 'goal-tp' : 'goal-target'}">${d.goal_source === 'TP' ? 'TP' : 'קונצנזוס'}</span>` : ''}</td>
      <td data-raw="${d.upside_pct ?? ''}">${d.upside_pct !== null ? (d.upside_pct > 0 ? '+' : '') + d.upside_pct.toFixed(1) + '%' : '—'}${lowConf && d.upside_pct !== null ? ' <span class="low-conf">⚠ כיסוי דל</span>' : ''}</td>
      <td data-raw="${d.profit_from_entry_pct ?? ''}">${d.profit_from_entry_pct !== null ? (d.profit_from_entry_pct > 0 ? '+' : '') + d.profit_from_entry_pct.toFixed(1) + '%' : '—'}</td>
      <td class="rating" data-raw="${d.rating || ''}">${d.rating || '—'}${d.coverage ? ` (${d.coverage})` : ''}</td>
      <td data-raw="${d.months_to_goal ?? 999999}">${fmtMonths(d.months_to_goal, d.goal_note)}</td>
    </tr>`;
  }).join('');
}

function updateStats(rows) {
  document.getElementById('statCount').textContent = rows.length;
  const totalInvested = rows.reduce((s, d) => s + (d.invested || 0), 0);
  document.getElementById('statInvested').textContent = '$' + Math.round(totalInvested).toLocaleString('en-US');
  document.getElementById('statTP').textContent = rows.filter(d => d.goal_source === 'TP').length;
  const withUpside = rows.filter(d => d.upside_pct !== null);
  const avgUpside = withUpside.length ? withUpside.reduce((s, d) => s + d.upside_pct, 0) / withUpside.length : 0;
  document.getElementById('statUpside').textContent = (avgUpside > 0 ? '+' : '') + avgUpside.toFixed(1) + '%';
  const potential = rows.reduce((s, d) => {
    if (d.goal === null || !d.price) return s;
    return s + (d.goal - d.price) * (d.units || 0);
  }, 0);
  document.getElementById('statPotential').textContent = '$' + Math.round(potential).toLocaleString('en-US');
}

render(DATA);
updateStats(DATA);

const table = document.getElementById('tbl');
const headers = table.querySelectorAll('th');
let sortCol = 12, sortDir = 'asc';

function applySort(colIdx, type, dir) {
  const rows = Array.from(document.getElementById('tbody').querySelectorAll('tr'));
  if (colIdx !== 0) {
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
  }
  const tbody = document.getElementById('tbody');
  rows.forEach((r, i) => {
    tbody.appendChild(r);
    const rn = r.children[0];
    rn.textContent = i + 1;
    rn.dataset.raw = i + 1;
  });
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
    else { sortCol = colIdx; sortDir = 'asc'; }
    applySort(sortCol, type, sortDir);
  });
});

applySort(sortCol, 'num', sortDir);
</script>
</body>
</html>
"""


def get_attr(block, attr):
    m = re.search(attr + r'="([^"]*)"', block)
    return m.group(1) if m else ""


def load_tp(filename):
    tp = {}
    path = ROOT / filename
    if not path.exists():
        return tp
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                try:
                    tp[parts[0]] = float(parts[1])
                except ValueError:
                    pass
    return tp


def main():
    tp_map = load_tp("portfolio_tp.tsv")

    portfolio = []
    path = ROOT / "portfolio_virtual.tsv"
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
                portfolio.append((ticker, {
                    "name": name,
                    "units": float(units),
                    "avgopen": float(avgopen),
                    "pl_dollar": float(pl),
                    "plpct": float(plpct),
                    "netvalue": float(netvalue),
                }))
            except ValueError:
                continue

    html = (ROOT / "all_rows.html").read_text(encoding="utf-8")

    out = []
    for ticker, d in portfolio:
        m = re.search(r'<tr data-ticker="' + re.escape(ticker) + r'"[^>]*>', html)
        block = m.group(0) if m else ""
        price_s = get_attr(block, "data-price")
        avg_target_s = get_attr(block, "data-avg")
        yh_avg_s = get_attr(block, "data-yh-avg")
        rating = get_attr(block, "data-rating")
        currency = get_attr(block, "data-currency")
        coverage = get_attr(block, "data-coverage")

        price = float(price_s) if price_s else None
        target_raw = avg_target_s if avg_target_s else yh_avg_s
        target = float(target_raw) if target_raw else None

        entry = d["avgopen"]
        broken_target = (
            target is not None and price and price > 0 and target <= price
            and rating in ("Strong Buy", "Moderate Buy", "Buy")
        )
        if broken_target:
            target = None

        user_tp = tp_map.get(ticker)
        if user_tp:
            goal = user_tp
            goal_source = "TP"
        elif target:
            goal = target
            goal_source = "target"
        else:
            goal = None
            goal_source = None

        upside_pct = None
        if price and goal and price > 0:
            upside_pct = (goal - price) / price * 100.0

        profit_from_entry_pct = None
        if goal and entry > 0:
            profit_from_entry_pct = (goal - entry) / entry * 100.0

        months_to_goal = None
        goal_note = ""
        if broken_target and not user_tp:
            goal_note = "broken"
        elif not price or price <= 0:
            goal_note = "No live price"
        elif goal is None:
            goal_note = "No goal"
        elif goal <= price:
            goal_note = "Already at/above goal"
        elif goal_source == "target":
            # goal IS the 12-month analyst target by definition, so "months to
            # reach it" would always trivially compute to ~12 - not real info.
            # Show a fixed horizon label instead of a computed number.
            goal_note = "target_horizon"
        elif not target or target <= price:
            # no analyst-implied growth rate available to project a TP-only goal
            goal_note = "No goal"
        else:
            annual_r = (target - price) / price
            monthly_r = (1 + annual_r) ** (1 / 12) - 1
            if monthly_r <= 0:
                goal_note = "No goal"
            else:
                months_to_goal = round(math.log(goal / price) / math.log(1 + monthly_r), 1)

        # invested must come from netvalue-pl_dollar, NOT units*entry: entry is
        # the raw local-currency quote price for foreign tickers (e.g. GBX
        # pence for .L tickers), so units*entry silently produces a wildly
        # inflated non-USD number for anything not quoted in USD (found live
        # 2026-09-19 via several .L/.DE tickers off by ~75-100x this way).
        # netvalue/pl_dollar are both already in account currency (USD).
        pl_dollar = round(d["pl_dollar"], 2)
        netvalue = round(d["netvalue"], 2)
        invested = round(netvalue - pl_dollar, 2)

        out.append({
            "ticker": ticker,
            "name": d["name"],
            "units": d["units"],
            "entry": entry,
            "price": price,
            "plpct": round(d["plpct"], 2),
            "invested": invested,
            "pl_dollar": pl_dollar,
            "netvalue": netvalue,
            "goal": round(goal, 4) if goal is not None else None,
            "goal_source": goal_source,
            "upside_pct": round(upside_pct, 1) if upside_pct is not None else None,
            "profit_from_entry_pct": round(profit_from_entry_pct, 1) if profit_from_entry_pct is not None else None,
            "rating": rating,
            "coverage": coverage,
            "months_to_goal": months_to_goal,
            "goal_note": goal_note,
            "currency": currency,
        })

    out.sort(key=lambda r: r["months_to_goal"] if r["months_to_goal"] is not None else 999999)

    import datetime
    gen_date = datetime.date.today().strftime("%d/%m/%Y")

    page = TEMPLATE.replace("__DATA_JSON__", json.dumps(out, ensure_ascii=False, indent=2))
    page = page.replace("__GEN_DATE__", gen_date)

    (ROOT / "exit_plan_report.html").write_text(page, encoding="utf-8")
    print(f"Wrote exit_plan_report.html ({len(out)} Virtual positions)")


if __name__ == "__main__":
    main()
