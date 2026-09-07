# Stockholm Stock List Project — Handoff Log

**Read this file, then `STOCKHOLM_LETTER_STATUS.md`.** Sixth sibling project — NASDAQ (`PROJECT_LOG.md`), NYSE (`NYSE_PROJECT_LOG.md`), Frankfurt (`FRANKFURT_PROJECT_LOG.md`), Paris (`PARIS_PROJECT_LOG.md`), Sydney (`SYDNEY_PROJECT_LOG.md`), now Stockholm. Same v4 methodology, separate output files.

## ⚠️ Policy: runs IN PARALLEL with NYSE, Frankfurt, Paris, and Sydney, by explicit user decision 2026-08-26

Same exception as the others — user explicitly chose to run five exchanges simultaneously despite the compounding eToro rate-limit/lockout risk. **Confirmed 2026-08-26**: after Frankfurt/Paris/Sydney all hit an ordinary-lockout block within minutes of each other, a direct AAPL check showed the eToro account was logged out account-wide (not per-tab) — "Delayed prices", "Research information is only available to active investors / Sign up". This strongly suggests these blocks are account-session-level, not IP/tab-level, so running more parallel agents increases how fast the shared account gets logged out, even though it doesn't seem to be a hard Cloudflare IP ban in this case. **Do not start real work until the coordinating session has confirmed a fresh, verified login** (this file's setup doesn't require login, only the actual per-ticker scraping does).

Each agent must use its own dedicated fresh browser tab(s) — never share/reuse another agent's tab (known cross-talk failure mode in this project family). On any block: stop immediately, don't retry/solve, checkpoint, report back.

## The goal

Same as the others: analyst Low/Average/High price target + tradeability per Stockholm-listed stock on eToro, via the **v4 text-based method** (see `PROJECT_LOG.md`'s "v4 METHOD UPDATE" section — read in full).

v4 method quick summary:
- Analyst Low/Avg/High: navigate to `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, `get_page_text`. "This stock has no research data" = NOFAQ. Stockholm tickers carry a `.ST` suffix (e.g. `EVO.ST`) — keep it. Note some tickers contain a hyphen or underscore (e.g. `ATCO-B.ST`, `NDA_SE.ST`) — pass them through as-is, don't strip/modify.
- Price + tradeability: navigate to `https://www.etoro.com/markets/{ticker-lower}/research` (keep `.st` suffix in URL), `get_page_text` for price, javascript_exec for tradeability: `Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.trim()==='Trade').map(b=>b.disabled)` — false=TRADEABLE, true=NOT_TRADEABLE.
- Mandatory human-paced protocol: randomized 3-8s per ticker, batches of 12-15 then randomized 30-50s pause. Lean conservative — five simultaneous agents share the same eToro account.
- Rigorously verify eToro login before starting (AAPL check) — given the account-wide lockout risk noted above, this check matters even more than usual here.

## Starting point: `stockholm_data.tsv` — built 2026-08-26 from a user-provided CSV export

- User exported eToro's Stockholm screener to `H:\קלוד\הורדות\סטקהולם.csv`.
- Built into `stockholm_data.tsv`: same 6-column format (`TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`), sorted alphabetically by ticker. **160 unique tickers, 0 duplicates**.
- **Consensus%/Rating columns blank** — same limitation as the other CSV-based imports.
- Ticker format: `.ST` suffix, some with `-A`/`-B` share-class suffixes or underscores (e.g. `SEB-A.ST`, `NDA_SE.ST`) — keep exactly as in the tsv. Letter distribution reasonable (largest S=28, A=21) — **no letter needs splitting**.
- One K-notation price spotted in the source data (`ROKOb.ST` shown as `1.89K`) — same known quirk as other exchanges' imports (approximate, real price comes from the per-ticker Analysis-tab visit anyway).

## File naming convention

- Output: `analyst_targets_STOCKHOLM_<LETTER>.txt`.
- Session log: `SESSION_LOG_STOCKHOLM_<LETTER>.md`.
- Claim board: `STOCKHOLM_LETTER_STATUS.md`.
- Master data: `stockholm_data.tsv`.

## Completeness audit

Same technique as the other projects: diff every ticker in the letter's slice of `stockholm_data.tsv` against the output file, both directions, before declaring done.

## The eventual site

Own standalone HTML page mirroring `nasdaq-stocks.html`, built once enough letters are done and the user asks.
