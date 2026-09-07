# Session Log — NYSE Letter A

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High analyst data, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). No screenshots/zoom used.

**Login verification**: AAPL checked before starting — real-time price (309.80, off-hours delta), "Prices by NASDAQ, in USD" (not delayed), Trade button enabled, tipranks AAPL data (245.00/337.09/400.00) matched known-real NASDAQ-project data exactly. Login confirmed good.

**Tickers**: 165, sourced from `grep '^A' nyse_data.tsv`, sorted.

**Pacing**: randomized 3-6s waits per ticker, batches of ~2-4 tickers per browser_batch call, randomized ~38-40s pause every 2-5 tickers (roughly every batch of 12-15 within the human-paced protocol's guidance, adjusted for how many tickers a browser_batch call covered).

**Blocks encountered**: None. One transient "Chrome extension disconnected" error mid-session (recovered automatically on retry, tabs intact, no data lost).

**Results**: 165/165 tickers completed.
- OK/TRADEABLE: 154
- OK/NOT_TRADEABLE: 4 (ADIG, AAPL.24-7, AMZN.24-7 — CFD 24/7 instruments with disabled Trade buttons; AZUL — OTC Markets listing, disabled Trade buttons)
- NOFAQ: 7 (AEG, AEXA, AIV, ALUR, ARR, AVD, AXIAY — mostly SPACs/foreign-listed/thinly-covered names; "This stock has no research data" from tipranks widget)

NOFAQ rate: 7/165 = 4.2% — somewhat below the 10-20% range seen on some NASDAQ letters, but not anomalous (no signs of fabrication — every row was read from live get_page_text output, prices/targets vary naturally per ticker, matches spot-checked against known-real AAPL/A data).

**Completeness audit**: `grep '^A' nyse_data.tsv` (165 tickers) vs `analyst_targets_NYSE_A.txt` (165 lines) — diffed both directions with `comm`, zero misses either way, zero duplicate tickers in output.

**Special cases**:
- `.US`/`.CH`/`.24-7` suffixes kept in eToro URL slugs (stripping them redirects to /home) — confirmed working for A.US, ABT.US, AIR.US, AMP.US, ATHM.CH, AVNT.US, AXS.US, AERO.US, ACA.US, AKA.US, AR.US, ASR (no suffix needed, ticker matched directly).
- No CVR-type tickers found in letter A.
- AAPL.24-7 / AMZN.24-7: 24/7 CFD trading instruments of the underlying stock — recorded with the underlying's own analyst data (via tipranks lookup on the base ticker AAPL/AMZN) since the CFD product itself has no separate analyst coverage, and both showed Trade buttons disabled → NOT_TRADEABLE.

Status board and file updated. Moving to letter B automatically per orchestration policy.
