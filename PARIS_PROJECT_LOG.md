# Paris Stock List Project — Handoff Log

**Read this file, then `PARIS_LETTER_STATUS.md`.** Fourth sibling project — NASDAQ (`PROJECT_LOG.md`), NYSE (`NYSE_PROJECT_LOG.md`), Frankfurt (`FRANKFURT_PROJECT_LOG.md`), now Paris. Same v4 methodology, separate output files.

## ⚠️ Policy: runs IN PARALLEL with NYSE and Frankfurt, by explicit user decision 2026-08-26

Same exception as Frankfurt's — user explicitly chose to run three exchanges simultaneously despite the doubled/tripled eToro rate-limit risk (a real Cloudflare 1015 block already happened once this session on NYSE, even under the v4 method — v4 makes each ticker cheaper in tokens/time, it does **not** reduce request volume or block risk). Each agent (NYSE, Frankfurt, Paris) must use its own dedicated fresh browser tab(s) — never share/reuse another agent's tab (known cross-talk failure mode in this project family). On any block: stop immediately, don't retry/solve, checkpoint, report back.

## The goal

Same as the other three: analyst Low/Average/High price target + tradeability per Paris-listed stock on eToro, via the **v4 text-based method** (see `PROJECT_LOG.md`'s "v4 METHOD UPDATE" section — read in full).

v4 method quick summary:
- Analyst Low/Avg/High: navigate to `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, `get_page_text`. "This stock has no research data" = NOFAQ. Paris tickers carry a `.PA` suffix (e.g. `AIR.PA`) — keep it.
- Price + tradeability: navigate to `https://www.etoro.com/markets/{ticker-lower}/research` (keep `.pa` suffix in URL), `get_page_text` for price, javascript_exec for tradeability: `Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.trim()==='Trade').map(b=>b.disabled)` — false=TRADEABLE, true=NOT_TRADEABLE.
- Mandatory human-paced protocol: randomized 3-8s per ticker, batches of 12-15 then randomized 30-50s pause. Lean conservative given three simultaneous agents now share the same eToro account/IP.
- Rigorously verify eToro login before starting (AAPL check).

## Starting point: `paris_data.tsv` — built 2026-08-26 from a user-provided CSV export

- User exported eToro's Paris screener to `H:\קלוד\הורדות\פאריס.csv`.
- Built into `paris_data.tsv`: same 6-column format (`TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`), sorted alphabetically by ticker. **416 unique tickers, 0 duplicates** (verified directly against the CSV).
- **Consensus%/Rating columns blank** — same limitation as Frankfurt's import, source CSV didn't include those columns. Doesn't block per-ticker scraping.
- Ticker format: `.PA` suffix. **Letter "A" is unusually large (185 of 416 tickers)** because Euronext Growth Paris small-caps commonly use an `AL`-prefixed ticker convention (ALAFY, ALAGO, ALODC, etc.) — this is real, not a data error. Split into three sub-groups in `PARIS_LETTER_STATUS.md`: **A1** (AB.PA–ALESE.PA, 62 tickers), **A2** (ALFER.PA–ALODC.PA, 62 tickers), **A3** (ALOKW.PA–AYV.PA, 61 tickers) — same split pattern as NASDAQ's M1/M2, P1/P2, S1/S2.

## File naming convention

- Output: `analyst_targets_PARIS_<GROUP>.txt` (groups: A1, A2, A3, B, C, ... Z, plus a `7` bucket for the one digit-leading ticker `74SW.PA`).
- Session log: `SESSION_LOG_PARIS_<GROUP>.md`.
- Claim board: `PARIS_LETTER_STATUS.md`.
- Master data: `paris_data.tsv`.

## Completeness audit

Same technique as the other three projects: diff every ticker in the group's slice of `paris_data.tsv` against the output file, both directions, before declaring done.

## The eventual site

Own standalone HTML page mirroring `nasdaq-stocks.html`, built once enough groups are done and the user asks.
