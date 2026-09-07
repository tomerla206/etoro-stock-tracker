# Hong Kong Stock List Project — Handoff Log

**Read this file, then `HONGKONG_LETTER_STATUS.md`.** Seventh sibling project — NASDAQ (`PROJECT_LOG.md`), NYSE, Frankfurt, Paris, Sydney, Stockholm, now Hong Kong. Same v4 methodology, separate output files.

## ⚠️ Policy: SEQUENTIAL, not parallel — one exchange project active at a time

**Different from the Frankfurt/Paris/Sydney/Stockholm launch policy.** After running NYSE+Frankfurt+Paris+Sydney+Stockholm in parallel caused repeated fast account-wide ordinary-lockout blocks (2026-08-26), the user explicitly asked to switch to running all sibling exchange projects **one at a time, in order**, instead of simultaneously. Hong Kong joins the back of that queue (after NYSE, Frankfurt, Paris, Sydney, Stockholm each get worked through). Do not launch a Hong Kong agent while another sibling project's agent is still active — check with the coordinating session first.

## The goal

Same as the others: analyst Low/Average/High price target + tradeability per Hong Kong-listed stock on eToro, via the **v4 text-based method** (see `PROJECT_LOG.md`'s "v4 METHOD UPDATE" section — read in full).

v4 method quick summary:
- Analyst Low/Avg/High: navigate to `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, `get_page_text`. "This stock has no research data" = NOFAQ. Hong Kong tickers carry a `.HK` suffix (e.g. `00700.HK` for Tencent) — keep it.
- Price + tradeability: navigate to `https://www.etoro.com/markets/{ticker-lower}/research` (keep `.hk` suffix in URL), `get_page_text` for price, javascript_exec for tradeability: `Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.trim()==='Trade').map(b=>b.disabled)` — false=TRADEABLE, true=NOT_TRADEABLE.
- Mandatory human-paced protocol: randomized 3-8s per ticker, batches of 12-15 then randomized 30-50s pause.
- Rigorously verify eToro login before starting (AAPL check).
- Note: Hong Kong trading hours are offset from other markets — closed/after-hours pricing is normal, not a problem sign.

## Starting point: `hongkong_data.tsv` — built 2026-08-26 from a user-provided CSV export

- User exported eToro's Hong Kong screener to `H:\קלוד\הורדות\הונגקונג.csv`.
- Built into `hongkong_data.tsv`: same 6-column format (`TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`), sorted alphabetically (= numerically, since every ticker is digit-leading) by ticker. **232 unique tickers, 0 duplicates**.
- **Consensus%/Rating columns blank** — same limitation as the other CSV-based imports.
- Ticker format: `.HK` suffix, all tickers are purely numeric codes (e.g. `00001.HK`, `9988.HK`) with inconsistent zero-padding in the source data (some 5-digit like `00001.HK`, some unpadded like `12.HK`) — **kept exactly as eToro exports them**, don't renormalize padding.
- **Unlike every other exchange in this project, letter-based grouping doesn't apply** (nothing to group by — everything starts with a digit). Split into **6 roughly-equal sequential groups of ~39 tickers each** (HK1 through HK6, in the tsv's sorted order) purely for manageable batch sizes, no alphabetic meaning.

## File naming convention

- Output: `analyst_targets_HONGKONG_<GROUP>.txt` (groups: HK1–HK6).
- Session log: `SESSION_LOG_HONGKONG_<GROUP>.md`.
- Claim board: `HONGKONG_LETTER_STATUS.md`.
- Master data: `hongkong_data.tsv`.

## Completeness audit

Same technique as the other projects: diff every ticker in the group's slice of `hongkong_data.tsv` against the output file, both directions, before declaring done.

## The eventual site

Already covered by the existing multi-exchange site (`nasdaq-stocks.html`, titled "Global Stock Snapshot" as of 2026-08-26) — its exchange-filter pills auto-generate from each row's `data-exchange` value, so adding Hong Kong just needs `generate_exchange_rows.py` extended with `("hongkong_data.tsv", "Hong Kong")` and a re-run of the merge, same process used for NYSE/Frankfurt/Paris/Sydney/Stockholm.
