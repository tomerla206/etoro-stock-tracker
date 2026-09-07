# Refresh Log — Chunk 8 (green tickers, 298 total)

Source list: `refresh_green_chunk_08.tsv` (ARB.ASX ... 2601.HK). Method per `REFRESH_METHOD.md` — TipRanks widget at `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, no suffix-stripping needed for this chunk (all tickers were `.ASX`, `.ST`, or `.HK`, none of which are in the strip list).

## Coverage
- Sydney (ASX): 188 tickers (ARB.ASX through YAL.ASX) — all processed.
- Stockholm (ST): 39 tickers (AAK.ST through YUBICO.ST) — all processed.
- Hong Kong (HK): 71 tickers (0386.HK through 2601.HK) — all processed.
- **Total: 298/298 processed.**

## Anomalies / notes
- **GMG.ASX**: first `innerText`-based extraction attempt returned NOSECTION (likely a timing/render hiccup); re-fetched successfully via `get_page_text` on the same page load. Data was present, just missed by the quick JS snippet that run.
- **CIP.ASX, DRO.ASX, PWH.ASX, MP1.ASX, WEB.ASX, 1772.HK, 1339.HK**: analyst count/spread dropped noticeably vs. the old stored value (e.g. from a multi-analyst spread down to a single-analyst consensus, or vice versa) — these are genuine data changes from TipRanks, not extraction errors; updated as scraped.
- **2513.HK (Knowledge Atlas Technology JSC Ltd)**: large jump from ~1090/1400/1500 to a flat 1985/1985/1985 (single analyst now) — verified via widget, looks like a real analyst re-rating, left as scraped.
- **1288.HK, 2328.HK**: old stored values were noticeably stale/out of range vs. new consensus (e.g. Low/Avg/High moved from ~6.2-6.6 to 7.10 flat, and from 15.50 flat to 16.80-20.00) — updated per widget.
- No tickers had "no research data" / lost coverage in this chunk — all 298 retained real TipRanks coverage.
- No malformed existing rows found beyond ordinary staleness (Low/Avg/High drift).
- One transient note: `analyst_targets_SYDNEY_A.txt` was seen to change on disk mid-run (another chunk's concurrent edits to different tickers in the same file, e.g. AD8.ASX, AGL.ASX, etc. — alphabetically before this chunk's ARB.ASX+). Not a conflict; different rows, left as-is.

## Pacing
15-20s randomized wait between every ticker (two `computer:wait` calls per cycle, e.g. 9s+8s, 10s+7s, etc., varied each time per instructions), using the same dedicated browser tab for the whole chunk.

## Summary
**298/298 processed, ~180 rows updated with fresh Low/Avg/High values, 0 flagged lost-coverage.**
