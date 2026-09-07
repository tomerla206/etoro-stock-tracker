# Milan Stock List Project — Handoff Log

**Read this file, then `MILAN_LETTER_STATUS.md`.** Tenth sibling project — NASDAQ (`PROJECT_LOG.md`), NYSE, Frankfurt, Paris, Sydney, Stockholm, Hong Kong, Oslo, Tokyo, now Milan. Same v4 methodology, separate output files.

## ⚠️ Policy: SEQUENTIAL, not parallel — one exchange project active at a time

Same as the other queued exchanges: after the earlier full-parallel run caused repeated fast account-wide ordinary-lockout blocks (2026-08-26), the user asked to run all sibling exchange projects one at a time, in order. Milan joins the back of that queue. Do not launch a Milan agent while another sibling project's agent is still active — check with the coordinating session first.

## The goal

Same as the others: analyst Low/Average/High price target + tradeability per Milan-listed stock on eToro, via the **v4 text-based method** (see `PROJECT_LOG.md`'s "v4 METHOD UPDATE" section — read in full).

v4 method quick summary:
- Analyst Low/Avg/High: navigate to `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, `get_page_text`. "This stock has no research data" = NOFAQ. Milan tickers carry a `.MI` suffix (e.g. `ENI.MI`) — keep it.
- Price + tradeability: navigate to `https://www.etoro.com/markets/{ticker-lower}/research` (keep `.mi` suffix in URL), `get_page_text` for price, javascript_exec for tradeability: `Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.trim()==='Trade').map(b=>b.disabled)` — false=TRADEABLE, true=NOT_TRADEABLE.
- Mandatory human-paced protocol: randomized 3-8s per ticker, batches of 12-15 then randomized 30-50s pause.
- Rigorously verify eToro login before starting (AAPL check).

## Starting point: `milan_data.tsv` — built 2026-08-26 from a user-provided CSV export

- User exported eToro's Milan screener to `H:\קלוד\הורדות\מילאן.csv`.
- Built into `milan_data.tsv`: same 6-column format (`TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`), sorted alphabetically by ticker. **78 unique tickers, 0 duplicates** — the smallest exchange in this project family so far.
- **Consensus%/Rating columns blank** — same limitation as most CSV-based imports.
- Ticker format: `.MI` suffix. Letter distribution is small and even (largest is I/B/A/S at 8-9 each) — **no letter needs splitting**, and the whole exchange could plausibly be worked as a single session.

## File naming convention

- Output: `analyst_targets_MILAN_<LETTER>.txt`.
- Session log: `SESSION_LOG_MILAN_<LETTER>.md`.
- Claim board: `MILAN_LETTER_STATUS.md`.
- Master data: `milan_data.tsv`.

## Completeness audit

Same technique as the other projects: diff every ticker in the letter's slice of `milan_data.tsv` against the output file, both directions, before declaring done.

## The eventual site

Already covered by the existing multi-exchange site (`nasdaq-stocks.html`, titled "Global Stock Snapshot") — extend `generate_exchange_rows.py`'s `EXCHANGES` list with `("milan_data.tsv", "Milan")` and re-run the merge, same process used for the other exchanges.
