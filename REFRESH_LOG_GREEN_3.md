# Refresh Log — Green Chunk 3

Chunk 3 of 11 parallel chunks refreshing analyst Low/Avg/High targets for the 4,330 currently-tradeable-with-coverage ("green") tickers. Source list: `refresh_green_chunk_03.tsv` (416 tickers, NASDAQ 1-309 + NYSE 310-416).

Method: TipRanks widget (`https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`), per `REFRESH_METHOD.md`. Own dedicated Chrome tab reused for all 416 tickers. Paced 15-20s (varied) between tickers throughout.

## Suffix-stripping notes

Stripped `.US` suffix before querying (kept original suffixed form as output key) for: `INV.US`, `ALLT.US`, `QNT.US`, `A.US`, `ABT.US`, `ACA.US`, `ACH.US`, `AERO.US`, `AIR.US`, `AKA.US`, `AMP.US`.

`SPCX.24-7` — not a suffix pattern explicitly listed in the method doc (not `.US/.A/.B/.EUR` or `/V`), but clearly an internal disambiguator (24/7 CFD-availability tag) on a NASDAQ-listed US stock, so treated the same way: stripped to `SPCX` for querying, kept `SPCX.24-7` as the output key. Reused the same scraped values as the separate `SPCX` line elsewhere in the list (both resolve to the same underlying Space Exploration Technologies Corp instrument on TipRanks).

## Anomalies / edge cases

- No tickers showed "no research data" or a missing ANALYST PRICE TARGET section — zero lost-coverage cases in this chunk, nothing flagged for manual review.
- All 416 tickers had the standard aggregated LOW ESTIMATE / AVERAGE PRICE TARGET / HIGH ESTIMATE box; no individual-ratings-only (widget-format-variant) cases requiring manual min/mean/max computation.
- One early batch of tickers (RELL, IMRX, IPX, RCMT, STOK, NVCT, ZVRA) was scraped via an oversized single browser-automation batch call that hit a tool timeout mid-execution; navigation had silently continued in the background past the reported error. To be safe, all of those tickers except the one directly re-verified (INVE) were re-scraped individually before being recorded, so no unverified data made it into the log or the files.
- All 416 scraped tickers were successfully matched to a source line (first tab-separated field) across the `analyst_targets_*.txt` files (excluding `_OLD` files) — no orphan tickers.

## Update method

Scraped values were collected into a scratchpad TSV (`chunk03_scraped.tsv`) as the run progressed, then applied in bulk via a small Python script that located each ticker's line (by exact first-field match) in the appropriate `analyst_targets_*.txt` file and replaced only fields 4/5/6 (Low/Avg/High) in place, leaving Name, Price, AnalysisStatus, and TradeStatus untouched. Verified via spot-checks after the update (CRMD, A.US, APTV, SPCX.24-7, INV.US all confirmed correct).

## Summary

**416/416 processed, 416 updated, 0 flagged lost-coverage.**

Files touched (analyst_targets_*.txt, letter/section-organized): A, B, C, D, E, F, G, H, I, J, K, L, M1, M2, N, NYSE_A, O, P1, P2, Q, R, S1, S2, T, U, V, W, X, Y, Z.
