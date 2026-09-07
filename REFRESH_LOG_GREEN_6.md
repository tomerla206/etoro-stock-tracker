# Refresh Log — Chunk 6 (Green Tickers)

Method: `REFRESH_METHOD.md` — TipRanks widget, 15-20s randomized pacing, dedicated tab (id 1160642924, closed at end).

Ticker list: `refresh_green_chunk_06.tsv` (485 tickers, NYSE + a handful of Frankfurt at the tail).

## Summary

**485/485 processed, 484 updated, 1 flagged lost-coverage, 0 not-found.**

All scraped Low/Avg/High values were written into the matching line (fields 4/5/6) of whichever `analyst_targets_*.txt` file contained that ticker, via a batch Python script cross-referencing the full results set against every non-`_OLD` `analyst_targets_*.txt` file. No other fields (Name, Price, AnalysisStatus, TradeStatus) were touched.

## Anomalies

- **WPP** — TipRanks widget returned "This stock has no research data" (confirmed via direct page-text check, not just a load-timing false negative). Left unchanged in its source file per instructions; needs manual review / potential conversion to NOFAQ by a human or the audit process.
- All other 484 tickers returned a clean aggregated LOW ESTIMATE / AVERAGE PRICE TARGET / HIGH ESTIMATE box — no individual-analyst-only "widget-format variant" cases encountered in this chunk.
- Suffix stripping applied per method: `.US`, `.A` (PBR.A), `.EUR` (AAPL.EUR) stripped for querying but original suffixed ticker kept as the output key. Real exchange suffixes (`.DE` for the trailing Frankfurt tickers) queried as-is, unstripped.
- One transient Chrome-extension disconnect occurred mid-session (around ticker PD/PDM/PEB/PEG/PEN batch, and again briefly near ZTO/ZIP) — both times the extension reconnected on retry and the affected tickers were re-scraped cleanly with no data loss.
- No malformed existing rows encountered requiring manual fixes.

## Pacing

Randomized 15-20s wait between tickers throughout (implemented as two sub-10s `wait` calls per ticker, varied non-repeating combinations, since the tool caps a single wait at 10s).

## Final count

485/485 processed, 484 updated, 1 flagged lost-coverage (WPP), 0 tickers not found in the source files.
