# NYSE Stock List Project — Handoff Log

**Read this entire file before doing anything, then read `NYSE_LETTER_STATUS.md`.** This is the NYSE sibling project to the NASDAQ one (`PROJECT_LOG.md` / `LETTER_STATUS.md` / `analyst_targets_<LETTER>.txt` in this same directory) — same methodology, same proven techniques, different exchange and separate output files so the two never collide.

## ⚠️ Project-wide policy: ONE active chat/agent across BOTH exchanges at a time

This is the same policy already established for the NASDAQ project (see `PROJECT_LOG.md`) — it applies **across NASDAQ and NYSE combined**, not per-exchange. Before starting any NYSE letter, check whether a NASDAQ letter (or another NYSE letter) already has an active background agent running. Only one letter, on one exchange, should be actively being fetched from eToro at any given moment, project-wide.

## The goal, in one sentence

For every NYSE stock, add its analyst Low/Average/High price target and tradeability status — sourced from eToro's own per-stock Analysis tab (v3 method, same as NASDAQ) — one combined pass per stock, letter by letter.

## Starting point: `nyse_data.tsv` is already built and verified

Unlike the NASDAQ project (which needed an eToro-scroll phase to build its master ticker list from scratch), NYSE's master list was built directly from a set of TABON-style bulk CSV exports the user provided (`NYSE.csv` through `NYSE9.csv`, `NYSE924.csv`, `NYSE102.csv`, `305.csv`, `90.csv`, `5.csv`, all in `H:\קלוד\הורדות\`), cross-checked against eToro's own displayed count (~1,768) on 2026-08-23.

- **`nyse_data.tsv`** (this project directory) — same 6-column format as `nasdaq_data.tsv`: `TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`. **1,765 tickers, 0 duplicates.**
- Built from `NYSE3.csv` (the cleanest of the original 9 exports: 1,765 unique tickers, 0 duplicate rows — other exports either had scroll-duplication artifacts fully explained by this same set, or were smaller partial subsets fully contained within it).
- **Repeatedly re-verified 2026-08-23**: every subsequent CSV the user provided (`NYSE924.csv` 924 tickers, `NYSE102.csv` 102, `305.csv` 304, `90.csv` 90, `5.csv` 5) was checked and found to be a **complete subset** of `nyse_data.tsv` — zero new tickers found across all of them. Completeness is not in question.
- **Known data quirks fixed during import** (see `build_nyse_data.py` in this directory, reusable):
  - `BHA` (Biglari Holdings) appeared as `BHa` (mixed case) in the source CSV — normalized to uppercase.
  - **17 tickers had K-notation prices** in the source (e.g. `GS` as `"1.00K"`) — converted to full decimal (e.g. `1000.00`), but these are **approximate**, not eToro's real precise price (same "K-notation truncation" issue documented for NASDAQ). Precise prices will come from each ticker's own Analysis-tab visit during the per-letter combined pass, same as NASDAQ's price gets corrected there.
  - 13 tickers show price `0.00` — all confirmed legitimate: CVR-type merger tickers, or `...Q`-suffixed delisted/bankrupt tickers. Not parsing errors.

## The v3 methodology — identical to NASDAQ, just point it at NYSE tickers

**Read `PROJECT_LOG.md`'s "v3 methodology" and "Exact method for the Analysis tab — CONFIRMED 2026-08-23" sections — they apply exactly as written, exchange-agnostic.** In short:

1. Navigate to `https://www.etoro.com/markets/{ticker-lower}/research` (lands directly on the Analysis tab, works the same for NYSE tickers as NASDAQ ones — the URL pattern doesn't encode exchange).
2. The Low/Avg/High panel is a cross-origin iframe — must be read visually via `zoom`, not JS/accessibility-tree (same cross-origin limitation, confirmed exchange-agnostic).
3. Capture tradeability (green Trade button vs greyed/absent) and NOFAQ (no Analysis tab, or "This stock has no research data").
4. Output format, 8 columns, identical to NASDAQ v3: `TICKER<TAB>CompanyName<TAB>Price<TAB>Low<TAB>Avg<TAB>High<TAB>AnalysisStatus<TAB>TradeStatus`.

## ⚠️ MANDATORY human-paced protocol — read `PROJECT_LOG.md`'s section in full, it applies identically

Randomized 3-8s waits per ticker (never fixed), batches of 12-15 tickers with a real randomized 45-90s pause between batches, slight action variation. **Also read the lockout-escalation history** (ordinary login lockout → CAPTCHA → Cloudflare Error 1015 IP/session ban) — all block types are exchange-agnostic; the same eToro/Cloudflare anti-automation system covers the whole site, not just NASDAQ pages. Never attempt to solve a CAPTCHA or bypass Cloudflare. On any block: stop immediately, don't retry, don't attempt login, checkpoint cleanly, report back — the user will re-confirm login/wait out a Cloudflare ban as needed, same process as NASDAQ.

**Always rigorously verify the login precondition** before starting real work on any NYSE letter (account menu, green Trade button, "Prices by NASDAQ"/exchange-appropriate label not delayed, working Analysis tab with real numbers) — don't trust a bare "continue" from the user, the agent's own check is the real gate.

## File naming convention — distinct from NASDAQ to avoid collisions

- Output: **`analyst_targets_NYSE_<LETTER>.txt`** (e.g. `analyst_targets_NYSE_A.txt`) — note the `NYSE_` infix, distinguishing from NASDAQ's `analyst_targets_A.txt` etc. since both projects use A-Z letters.
- Session log: **`SESSION_LOG_NYSE_<LETTER>.md`**.
- Claim board: **`NYSE_LETTER_STATUS.md`** (this project directory), separate from NASDAQ's `LETTER_STATUS.md`.
- Master data: **`nyse_data.tsv`**, separate from `nasdaq_data.tsv`.

## Completeness-audit technique (proven on NASDAQ letters C, D, E — use it here too)

Before declaring any NYSE letter done, diff every ticker starting with that letter in `nyse_data.tsv` against the letter's `analyst_targets_NYSE_<LETTER>.txt` output, both directions — catches accidentally-skipped tickers (this caught 3 misses on NASDAQ letter C).

## The eventual site

NYSE will get its own standalone HTML page mirroring `nasdaq-stocks.html`'s design (row numbering, status filters, Upside % column with Low/Avg/High basis toggle, investment allocation calculator, P/L and % of Profit columns — see `part1_fixed.html`/`nasdaq_rows.html`/`part3.html` as the template to adapt) once enough NYSE letters are done and the user asks for the merge — not before, per the same "deliberate step, not automatic" policy as NASDAQ's `merge_analyst_targets.py`.

## Merging (do only when the user asks, once several NYSE letters are DONE)

Same process as NASDAQ's `merge_analyst_targets.py` (in this directory) — will need a `nyse`-specific variant or a parameterized version once this is actually needed, pointed at `analyst_targets_NYSE_*.txt` and a to-be-built `nyse-stocks.html` (its own template parts, adapted from the NASDAQ ones, or a shared page listing both exchanges — ask the user which they prefer when this stage is reached).
