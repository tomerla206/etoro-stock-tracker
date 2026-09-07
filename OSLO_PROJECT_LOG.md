# Oslo Stock List Project — Handoff Log

**Read this file, then `OSLO_LETTER_STATUS.md`.** Eighth sibling project — NASDAQ (`PROJECT_LOG.md`), NYSE, Frankfurt, Paris, Sydney, Stockholm, Hong Kong, now Oslo. Same v4 methodology, separate output files.

## ⚠️ Policy: SEQUENTIAL, not parallel — one exchange project active at a time

Same as Hong Kong's policy: after the earlier full-parallel run (NYSE+Frankfurt+Paris+Sydney+Stockholm) caused repeated fast account-wide ordinary-lockout blocks (2026-08-26), the user asked to run all sibling exchange projects one at a time, in order. Oslo joins the back of that queue. Do not launch an Oslo agent while another sibling project's agent is still active — check with the coordinating session first.

## The goal

Same as the others: analyst Low/Average/High price target + tradeability per Oslo-listed stock on eToro, via the **v4 text-based method** (see `PROJECT_LOG.md`'s "v4 METHOD UPDATE" section — read in full).

v4 method quick summary:
- Analyst Low/Avg/High: navigate to `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, `get_page_text`. "This stock has no research data" = NOFAQ. Oslo tickers carry a `.OL` suffix (e.g. `EQNR.OL`) — keep it. **One exception noted in the source data**: `VEND` (Vend Marketplaces ASA) has no `.OL` suffix at all — pass it through exactly as-is, don't add one.
- Price + tradeability: navigate to `https://www.etoro.com/markets/{ticker-lower}/research` (keep `.ol` suffix in URL where present), `get_page_text` for price, javascript_exec for tradeability: `Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.trim()==='Trade').map(b=>b.disabled)` — false=TRADEABLE, true=NOT_TRADEABLE.
- Mandatory human-paced protocol: randomized 3-8s per ticker, batches of 12-15 then randomized 30-50s pause.
- Rigorously verify eToro login before starting (AAPL check).

## Starting point: `oslo_data.tsv` — built 2026-08-26 from a user-provided CSV export

- User exported eToro's Oslo screener to `H:\קלוד\הורדות\אוסלו.csv`.
- Built into `oslo_data.tsv`: same 6-column format (`TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`), sorted alphabetically by ticker. **232 unique tickers, 0 duplicates**.
- **Consensus%/Rating columns blank** — same limitation as the other CSV-based imports.
- Ticker format: `.OL` suffix (one exception: `VEND`, no suffix — see above). Some tickers share a base name with a different share class/entity, e.g. `ODF.OL`/`ODFB.OL` (Odfjell SE, two listings) and `WWI.OL`/`WWIB.OL` (Wilh Wilhelmsen Holding, two listings) — both are real, distinct, keep both, not a duplicate-data bug.
- One K-notation price spotted (`AKER.OL` shown as `1.48K`) — same known quirk as other exchanges (real price comes from the per-ticker Analysis-tab visit anyway).
- Letter distribution reasonable (largest A=26, N=25, S=25) — **no letter needs splitting**. A handful of tickers start with a digit (`2020.OL`, `5PG.OL` — 2 total) — group them under a small `0-9` bucket like Frankfurt did.

## File naming convention

- Output: `analyst_targets_OSLO_<LETTER>.txt`.
- Session log: `SESSION_LOG_OSLO_<LETTER>.md`.
- Claim board: `OSLO_LETTER_STATUS.md`.
- Master data: `oslo_data.tsv`.

## Completeness audit

Same technique as the other projects: diff every ticker in the letter's slice of `oslo_data.tsv` against the output file, both directions, before declaring done.

## The eventual site

Already covered by the existing multi-exchange site (`nasdaq-stocks.html`, titled "Global Stock Snapshot") — extend `generate_exchange_rows.py`'s `EXCHANGES` list with `("oslo_data.tsv", "Oslo")` and re-run the merge, same process used for the other exchanges.
