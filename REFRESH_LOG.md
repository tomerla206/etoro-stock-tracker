# Analyst-Target Refresh — Master Log (Round 1)

**Purpose**: refresh Low/Avg/High for all 4,330 currently-confirmed TRADEABLE+OK tickers, per the standard method in `REFRESH_METHOD.md`. This is the first full refresh pass; going forward this should repeat roughly daily.

**Source list**: `refresh_4330_list.tsv` (TICKER, FILE columns — FILE tells each agent exactly which `analyst_targets_*.txt` to edit for that ticker).

**Split into 11 parallel chunks** (~394 each):
1. rows 2-395
2. rows 396-789
3. rows 790-1183
4. rows 1184-1577
5. rows 1578-1971
6. rows 1972-2365
7. rows 2366-2759
8. rows 2760-3153
9. rows 3154-3547
10. rows 3548-3941
11. rows 3942-4331

Each chunk updates its assigned analyst_targets_*.txt files DIRECTLY (Low/Avg/High columns only, in place) and logs to its own `REFRESH_LOG_<N>.md`.

## Consolidated status

(filled in as chunks report)

## FULL REFRESH COMPLETE (2026-09-01, overnight)

All 11 chunks of the Low/Avg/High refresh finished successfully across the night (with several relaunches after transient stalls/disconnects — all resumed cleanly from logged checkpoints). Notable findings:
- Several London tickers (AAL.L, AZN.L, BHP.L, BP.L, GSK.L) had values off by roughly 10-100x — a GBX-vs-GBP-style unit confusion from an earlier scrape — caught and corrected.
- Multiple sub-agents independently caught and corrected transient Chrome-extension disconnect artifacts (stale/cross-contaminated reads) before writing bad data — no known bad data made it into the files.
- A handful of tickers (COCP, WPP, MANU, HAFN, KNOP, STB.OL, BAMNB.NV, CENER.BR, ABVX.PA) appear to have genuinely LOST TipRanks coverage since the original scrape — left unchanged (not auto-converted to NOFAQ) and flagged here for manual review:
  - Are these real delistings/coverage drops, or transient TipRanks-side gaps? Worth a spot-check in a future session before deciding whether to reclassify them as NOFAQ.

Final merge run, `nasdaq-stocks.html` reassembled and verified: 4,330/6,761 tickers still TRADEABLE+OK (unchanged from before the refresh, as expected — this was a value refresh, not a status change).

## Dividend column — first pass complete (2026-09-01)

All 4 chunks (A-D) completed, covering all 4,330 target tickers. Final coverage: 4,324/4,330 (99.86%). 6 tickers could not be resolved on Yahoo Finance at all: EROC, EROK (ticker resolves to an unrelated company), LEN.DE, SAV.DE, TA1.DE (not listed on Yahoo), SPCX.24-7 (a CFD/24-7 trading variant with no standalone Yahoo listing). These are left without a dividend value — acceptable, matches the pattern of unmappable tickers seen elsewhere in this project.

Key method refinement discovered mid-scrape: Amsterdam (`.NV`) tickers needed mapping to Yahoo's `.AS` suffix specifically (not just stripped bare) — stripping bare can match an unrelated US company (e.g. bare `PNL` = Paringa Resources, but `PNL.AS` = the intended PostNL). Added to `REFRESH_METHOD.md` for future sessions.

Final merge run via `merge_yahoo_dividends.py`, reassembled and verified in-browser (no console errors, correct cell population and formatting, e.g. AAPL → 0.34%, WASH → 5.68%).

**This was a big overnight session** — 15 parallel/sequential background agents total across both tasks, run with the user's explicit overnight authorization. Both `nasdaq-stocks.html` and this log are up to date as of the morning.
