# Oslo 0-9 Session Log

Login verified 2026-08-29: AAPL research page showed real-time price "319.70 5.12 (1.63%)", "Prices by NASDAQ", Market Closed (normal after-hours). Sanity-checked `button.trade-button` selector on AAPL (2 matches, both enabled, matches generic-selector count) before starting real work, per the 2026-08-29 tradeability selector refinement note.

## Tickers (2 total, per oslo_data.tsv)

| Ticker | Name | Price (NOK) | Low/Avg/High | Tradeability |
|---|---|---|---|---|
| 2020.OL | 2020 Bulkers Ltd | 3.96 | NOFAQ (tipranks: "This stock has no research data") | TRADEABLE (button.trade-button: both disabled=false) |
| 5PG.OL | 5Th Planet Games A/S | 1.3600 | NOFAQ (tipranks: "This stock has no research data") | TRADEABLE (button.trade-button: both disabled=false) |

Both tickers scraped in a single short session (only 2 tickers total, well under batch-pause threshold). No blocks encountered. No CAPTCHA/lockout signatures seen.

## Completeness audit

`grep -P '^[0-9]' oslo_data.tsv` → 2020.OL, 5PG.OL. Both present in `analyst_targets_OSLO_0-9.txt`. Diff clean both directions. **Group 0-9: DONE (2/2).**
