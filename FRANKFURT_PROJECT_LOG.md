# Frankfurt Stock List Project — Handoff Log

**Read this file, then `FRANKFURT_LETTER_STATUS.md`.** Third sibling project to NASDAQ (`PROJECT_LOG.md`) and NYSE (`NYSE_PROJECT_LOG.md`) — same v4 methodology, separate output files so nothing collides.

## ⚠️ Policy change 2026-08-26 — this project runs IN PARALLEL with NYSE, by explicit user decision

Unlike the original NASDAQ/NYSE "one active agent across both exchanges" policy, the user explicitly asked to run Frankfurt at the same time as the ongoing NYSE work, after being told this doubles eToro rate-limit/block risk (a real Cloudflare 1015 block already happened once this session, on NYSE letter B, even using the v4 method — v4 makes each ticker cheaper in tokens/time, it does **not** reduce the number of requests sent to eToro/Cloudflare, so it doesn't by itself reduce block risk). User's reasoning: the v4 method is efficient/fast so risk is acceptable. Proceed accordingly, but:
- Each agent (NYSE, Frankfurt) must use its own dedicated browser tab(s) — never share/reuse a tab an unrelated agent might be driving (see the dual-agent tab cross-talk lesson in `PROJECT_LOG.md`).
- If either agent hits a block, it does not mean the other is also blocked (different content, same underlying IP/account) — but treat a block on one as a signal to be extra cautious on the other, and report it.
- On any block: stop immediately, don't retry/solve, checkpoint, report back — identical protocol to NASDAQ/NYSE.

## The goal

Same as NASDAQ/NYSE: for every Frankfurt-listed stock on eToro, add analyst Low/Average/High price target and tradeability status, sourced from eToro's own per-stock Analysis tab, using the **v4 text-based method** (see `PROJECT_LOG.md`'s "v4 METHOD UPDATE" section at the top — read that in full, don't rely on the summary below).

v4 method quick summary:
- Analyst Low/Avg/High: navigate to `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, use `get_page_text`. "This stock has no research data" = NOFAQ. Note Frankfurt tickers carry a `.DE` suffix (e.g. `SIE.DE`) — keep it in the ticker param, same as NASDAQ's `.US`/`.CH` suffix handling.
- Price + tradeability: navigate to `https://www.etoro.com/markets/{ticker-lower}/research` (keep the `.de` suffix in the URL slug — stripping it likely misroutes, same lesson as NASDAQ's `.US`/`.CH`), `get_page_text` for price, and this javascript_exec snippet for tradeability: `Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.trim()==='Trade').map(b=>b.disabled)` — false=TRADEABLE, true=NOT_TRADEABLE.
- Mandatory human-paced protocol unchanged: randomized 3-8s waits per ticker, batches of 12-15 then randomized 30-50s pause.
- Rigorously verify eToro login before starting (AAPL check).

## Starting point: `frankfurt_data.tsv` — built 2026-08-26 from a user-provided CSV export

- User exported the eToro Frankfurt screener (`https://www.etoro.com/discover/screener?InternalExchangeId=6`, confirmed 436 results on-screen) to `H:\קלוד\הורדות\פרנקפורט.csv`.
- Built into `frankfurt_data.tsv`: same 6-column format as `nasdaq_data.tsv`/`nyse_data.tsv` (`TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`), sorted alphabetically by ticker. **436 unique tickers, 0 duplicates** — verified against the CSV directly (row count and dedup check both matched the screener's on-screen "436 Results").
- **Consensus%/Rating columns are blank** — the source CSV export didn't include eToro's numeric consensus or rating-word columns (only price, dividend yield, avg volume, P/E ratio), unlike NASDAQ/NYSE's original imports. This doesn't block the per-ticker scraping work (which fetches Low/Avg/High/tradeability fresh per ticker regardless) — it only means the site's Consensus/Rating filter columns will show blank for Frankfurt unless backfilled later. Not a priority unless the user asks.
- Ticker format: `.DE` suffix (e.g. `SIE.DE`, `BAS.DE`). A handful of tickers start with digits (`0B2.DE`, `1FC.DE`, `2HRA.DE`, etc. — 14 total) — grouped under a `0-9` bucket in `FRANKFURT_LETTER_STATUS.md` rather than a real letter.

## File naming convention

- Output: `analyst_targets_FRANKFURT_<LETTER>.txt`.
- Session log: `SESSION_LOG_FRANKFURT_<LETTER>.md`.
- Claim board: `FRANKFURT_LETTER_STATUS.md`.
- Master data: `frankfurt_data.tsv`.

## Completeness audit

Same technique as NASDAQ/NYSE: before declaring any letter done, diff every ticker starting with that letter/bucket in `frankfurt_data.tsv` against the output file, both directions.

## The eventual site

Own standalone HTML page mirroring `nasdaq-stocks.html`, built once enough letters are done and the user asks — not automatic, same policy as NYSE.
