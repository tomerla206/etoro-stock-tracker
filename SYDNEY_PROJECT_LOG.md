# Sydney (ASX) Stock List Project — Handoff Log

**Read this file, then `SYDNEY_LETTER_STATUS.md`.** Fifth sibling project — NASDAQ (`PROJECT_LOG.md`), NYSE (`NYSE_PROJECT_LOG.md`), Frankfurt (`FRANKFURT_PROJECT_LOG.md`), Paris (`PARIS_PROJECT_LOG.md`), now Sydney. Same v4 methodology, separate output files.

## ⚠️ Policy: runs IN PARALLEL with NYSE, Frankfurt, and Paris, by explicit user decision 2026-08-26

Same exception as the other two — user explicitly chose to run four exchanges simultaneously despite the compounding eToro rate-limit risk (a real Cloudflare 1015 block already happened once this session on NYSE, even under the v4 method — v4 makes each ticker cheaper in tokens/time, it does **not** reduce request volume or block risk, and every parallel agent shares the same eToro account/IP). Each agent must use its own dedicated fresh browser tab(s) — never share/reuse another agent's tab (known cross-talk failure mode in this project family). On any block: stop immediately, don't retry/solve, checkpoint, report back.

## The goal

Same as the others: analyst Low/Average/High price target + tradeability per ASX-listed stock on eToro, via the **v4 text-based method** (see `PROJECT_LOG.md`'s "v4 METHOD UPDATE" section — read in full).

v4 method quick summary:
- Analyst Low/Avg/High: navigate to `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, `get_page_text`. "This stock has no research data" = NOFAQ. Sydney tickers carry a `.ASX` suffix (e.g. `BHP.ASX`) — keep it.
- Price + tradeability: navigate to `https://www.etoro.com/markets/{ticker-lower}/research` (keep `.asx` suffix in URL), `get_page_text` for price, javascript_exec for tradeability: `Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.trim()==='Trade').map(b=>b.disabled)` — false=TRADEABLE, true=NOT_TRADEABLE.
- Mandatory human-paced protocol: randomized 3-8s per ticker, batches of 12-15 then randomized 30-50s pause. Lean conservative — four simultaneous agents now share the same eToro account/IP.
- Rigorously verify eToro login before starting (AAPL check).
- Note: ASX trading hours are offset from NASDAQ/NYSE/European hours — a ticker showing as closed/after-hours is normal and not itself a sign of trouble, same as any other exchange's off-hours state.

## Starting point: `sydney_data.tsv` — built 2026-08-26 from a user-provided CSV export

- User exported eToro's Sydney/ASX screener to `H:\קלוד\הורדות\סידני.csv`.
- Built into `sydney_data.tsv`: same 6-column format (`TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`), sorted alphabetically by ticker. **221 unique tickers, 0 duplicates** (verified directly against the CSV).
- **Consensus%/Rating columns blank** — same limitation as Frankfurt/Paris imports, source CSV didn't include those columns. Doesn't block per-ticker scraping.
- Ticker format: `.ASX` suffix. Letter distribution is reasonable (largest are C=25, A=23, S=21) — **no group needed splitting**, unlike Frankfurt/Paris.

## File naming convention

- Output: `analyst_targets_SYDNEY_<LETTER>.txt`.
- Session log: `SESSION_LOG_SYDNEY_<LETTER>.md`.
- Claim board: `SYDNEY_LETTER_STATUS.md`.
- Master data: `sydney_data.tsv`.

## Completeness audit

Same technique as the other projects: diff every ticker in the letter's slice of `sydney_data.tsv` against the output file, both directions, before declaring done.

## The eventual site

Own standalone HTML page mirroring `nasdaq-stocks.html`, built once enough letters are done and the user asks.
