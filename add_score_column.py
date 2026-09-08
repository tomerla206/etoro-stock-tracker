"""One-time migration: insert new <td> placeholders at the end of every row
in all_rows.html. Idempotent - skips if already migrated. Mirrors
add_insider_column.py's approach exactly.

(This script has been reused/extended each time a new fundamentals column was
added - score-cell, short/rsi/pe, market cap, hedge fund activity, beta,
volume spike, peg/52-week range, secondary-score, risk-score, overallscore,
percentile-cell, roe/instown/currentratio, quick ratio/ROA/held-insiders
(Score) + gross margin/operating margin/FCF yield/analyst coverage/forward P-E
(Secondary Score), now a 4th score - Growth Score (its own composite cell,
placed among the other score cells) - plus P/B, EV/EBITDA, EV/Revenue,
Payout Ratio, EBITDA Margin, Cash-to-MCap, OCF Margin, Relative Strength,
Short Interest Trend, Float %, and Growth Score's own 3 raw inputs, appended
at the tail like every round before - rather than writing a fresh
near-identical migration script every time.)"""

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

# Second migration: Growth Score (a 4th, separate score alongside Score/
# Secondary Score/Risk Score) plus its own composite cell among the other
# score cells, and 12 more raw fundamentals columns (P/B, EV/EBITDA,
# EV/Revenue, Payout Ratio, EBITDA Margin, Cash-to-MCap, OCF Margin,
# Relative Strength, Short Interest Trend, Float %, and Growth Score's own
# 3 raw inputs) appended at the tail like every round before this one.
growthscore_marker = re.compile(r'(<td class="riskscore-cell col-riskscore[^"]*"[^>]*>[\s\S]*?</td>)(<td class="overallscore-cell)')
tail_marker = re.compile(r'(<td class="fwdpe-cell col-fwdpe[^"]*"[^>]*>[\s\S]*?</td>)(</tr>)')

if "growthscore-cell" in content:
    print("Growth Score migration already applied, skipping.")
else:
    gs_count = len(growthscore_marker.findall(content))
    content = growthscore_marker.sub(
        r'\1<td class="growthscore-cell col-growthscore empty">&ndash;</td>\2',
        content,
    )
    tail_count = len(tail_marker.findall(content))
    content = tail_marker.sub(
        r'\1<td class="relstrength-cell col-relstrength empty">&ndash;</td>'
        r'<td class="pb-cell col-pb empty">&ndash;</td>'
        r'<td class="evebitda-cell col-evebitda empty">&ndash;</td>'
        r'<td class="evrevenue-cell col-evrevenue empty">&ndash;</td>'
        r'<td class="payout-cell col-payout empty">&ndash;</td>'
        r'<td class="ebitdamargin-cell col-ebitdamargin empty">&ndash;</td>'
        r'<td class="cashmcap-cell col-cashmcap empty">&ndash;</td>'
        r'<td class="ocfmargin-cell col-ocfmargin empty">&ndash;</td>'
        r'<td class="shortinttrend-cell col-shortinttrend empty">&ndash;</td>'
        r'<td class="floatpct-cell col-floatpct empty">&ndash;</td>'
        r'<td class="epsgrowth5y-cell col-epsgrowth5y empty">&ndash;</td>'
        r'<td class="epsgrowthnextyear-cell col-epsgrowthnextyear empty">&ndash;</td>'
        r'<td class="earningsqgrowth-cell col-earningsqgrowth empty">&ndash;</td>\2',
        content,
    )
    with open("all_rows.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Inserted growthscore-cell into {gs_count} rows and 13 more raw fundamentals cells into {tail_count} rows")
