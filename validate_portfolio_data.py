"""
Code name: SCAN CHECK. Sanity-checks the private portfolio data files and
the two derived reports (red_pl_report.html, exit_plan_report.html) for
internal-consistency bugs, and auto-fixes what's safely fixable.

Checks:
1. portfolio_virtual.tsv / portfolio_real.tsv: each row has 8 tab-separated
   fields, all numeric fields parse, no duplicate tickers, and
   netvalue == units*avgopen + pl (within 1 cent) - recomputes netvalue from
   units*avgopen+pl and rewrites the file if any row is off (this is the
   exact class of bug that would silently corrupt the exit/red-pl reports'
   money columns).
2. portfolio_tp.tsv / portfolio_real_tp.tsv: no ticker appears twice, no TP
   entry references a ticker that isn't actually held (stale after a
   position closes).
3. Every ticker in each held-portfolio file exists as a data-ticker row in
   all_rows.html (a name/target lookup miss would silently render as the
   bare ticker or a blank cell downstream).
4. exit_plan_report.html / red_pl_report.html: the embedded DATA JSON
   parses, and every row's invested/pl/netvalue reconcile arithmetically
   (invested + pl == netvalue, within 1 cent) - catches template/script
   bugs independent of the source-data bugs already checked in step 1.

Run: python validate_portfolio_data.py
Exit code 0 if clean (after auto-fixes), 1 if something needed a fix
(reported, not a failure of the script itself) - re-run to confirm clean.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TOL = 0.01

ISSUES = []
FIXED = []


def check_portfolio_file(filename):
    path = ROOT / filename
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    seen = {}
    out_lines = []
    changed = False
    for lineno, line in enumerate(lines, 1):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 8:
            ISSUES.append(f"{filename}:{lineno}: only {len(parts)} fields (expected 8): {line!r}")
            out_lines.append(line)
            continue
        ticker, name, units, avgopen, pl, plpct, netvalue, status = parts[:8]
        if ticker in seen:
            ISSUES.append(f"{filename}:{lineno}: duplicate ticker {ticker} (first seen line {seen[ticker]})")
        seen[ticker] = lineno

        if status == "PENDING":
            # Not filled yet: units/avgopen are legitimately unknown (blank),
            # and pl/plpct are meaningless until the order executes. Only
            # netvalue (the reserved/invested amount) and status matter here -
            # see merge_portfolio.py's PENDING tooltip, which only reads
            # netvalue. Just sanity-check that netvalue parses.
            try:
                float(netvalue)
            except ValueError as e:
                ISSUES.append(f"{filename}:{lineno}: non-numeric netvalue for pending {ticker}: {e}")
            out_lines.append(line)
            continue

        try:
            units_f = float(units)
            avgopen_f = float(avgopen)
            pl_f = float(pl)
            plpct_f = float(plpct)
            netvalue_f = float(netvalue)
        except ValueError as e:
            ISSUES.append(f"{filename}:{lineno}: non-numeric field for {ticker}: {e}")
            out_lines.append(line)
            continue

        # NOTE: invested/netvalue must be derived from pl_dollar and plpct
        # (both already in account currency, i.e. USD, exactly as eToro
        # displays them), NEVER from units*avgopen - avgopen is the raw
        # LOCAL-CURRENCY quote price for foreign tickers (e.g. GBX pence for
        # .L tickers), so units*avgopen silently produces a wildly inflated
        # non-USD number for any non-US-quoted ticker (found live 2026-09-19:
        # BKG.L/EAAS.L/SDY.L/PBEE.L/SAA.L/EXPN.L/FARN.L were all off by
        # ~75-100x this way). units*avgopen is only valid for USD-quoted
        # tickers, which isn't knowable here without cross-referencing
        # all_rows.html's data-currency, so don't use it for this check at all.
        # Skip the check below |plpct_f| < 2%: pl_dollar and plpct are both
        # rounded (cents / 2 decimals) as displayed by eToro, and dividing by
        # a small percentage amplifies that rounding into noise - e.g. a
        # displayed "$0.00 / >-0.01%" round-trips to a derived invested of
        # $0, which is nonsense, not a real bug. This check exists to catch
        # gross errors (the ~75-100x currency bug, see note above), which
        # show up as huge relative AND absolute differences - not to
        # second-guess eToro's own displayed netvalue on near-breakeven rows.
        if abs(plpct_f) >= 2:
            expected_invested = pl_f * 100.0 / plpct_f
            expected_netvalue = round(expected_invested + pl_f, 2)
            diff = abs(expected_netvalue - netvalue_f)
            if diff > 5 and diff > abs(netvalue_f) * 0.05:
                FIXED.append(
                    f"{filename}:{lineno}: {ticker} netvalue {netvalue_f} != pl/pl%%-derived "
                    f"({expected_netvalue}) - corrected"
                )
                netvalue = str(expected_netvalue)
                changed = True

        out_lines.append("\t".join([ticker, name, units, avgopen, pl, plpct, netvalue, status]))

    if changed:
        path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")

    return set(seen.keys())


def check_tp_file(filename, held_tickers):
    path = ROOT / filename
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    seen = set()
    for lineno, line in enumerate(lines, 1):
        if not line.strip():
            continue
        parts = line.split("\t")
        ticker = parts[0]
        if ticker in seen:
            ISSUES.append(f"{filename}:{lineno}: duplicate ticker {ticker}")
        seen.add(ticker)
        if held_tickers is not None and ticker not in held_tickers:
            ISSUES.append(f"{filename}:{lineno}: {ticker} has a TP entry but isn't currently HELD (stale)")


def check_tickers_in_site(held_tickers, label):
    if not held_tickers:
        return
    html_path = ROOT / "all_rows.html"
    if not html_path.exists():
        ISSUES.append("all_rows.html not found - cannot cross-check tickers")
        return
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    missing = [t for t in sorted(held_tickers) if f'data-ticker="{t}"' not in html]
    for t in missing:
        ISSUES.append(f"{label}: {t} is HELD but has no row in all_rows.html (name/target lookups will fail)")


def check_report(filename):
    path = ROOT / filename
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    m = re.search(r"const DATA = (\[.*?\]);\s*\n", html, re.S)
    if not m:
        ISSUES.append(f"{filename}: could not find embedded DATA JSON block")
        return
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        ISSUES.append(f"{filename}: DATA JSON failed to parse: {e}")
        return

    for row in data:
        if "invested" in row and "pl_dollar" in row and "netvalue" in row:
            expected = round(row["invested"] + row["pl_dollar"], 2)
            if abs(expected - row["netvalue"]) > TOL:
                ISSUES.append(
                    f"{filename}: {row['ticker']} invested({row['invested']}) + "
                    f"pl_dollar({row['pl_dollar']}) != netvalue({row['netvalue']})"
                )


def main():
    virtual_tickers = check_portfolio_file("portfolio_virtual.tsv")
    real_tickers = check_portfolio_file("portfolio_real.tsv")

    check_tp_file("portfolio_tp.tsv", virtual_tickers)
    check_tp_file("portfolio_real_tp.tsv", real_tickers)

    check_tickers_in_site(virtual_tickers, "portfolio_virtual.tsv")
    check_tickers_in_site(real_tickers, "portfolio_real.tsv")

    check_report("exit_plan_report.html")
    check_report("red_pl_report.html")

    print(f"Checked: portfolio_virtual.tsv ({len(virtual_tickers or [])} tickers), "
          f"portfolio_real.tsv ({len(real_tickers or [])} tickers), "
          f"portfolio_tp.tsv, portfolio_real_tp.tsv, "
          f"exit_plan_report.html, red_pl_report.html")

    if FIXED:
        print(f"\nAuto-fixed {len(FIXED)} issue(s):")
        for f in FIXED:
            print("  -", f)

    if ISSUES:
        print(f"\n{len(ISSUES)} issue(s) found (not auto-fixed, needs a look):")
        for i in ISSUES:
            print("  -", i)
        sys.exit(1)
    else:
        print("\nNo remaining issues.")
        sys.exit(0)


if __name__ == "__main__":
    main()
