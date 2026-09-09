# Daily Analyst-Target Refresh — Standard Method

## `build_site.py` (added 2026-09-06) — the ONLY script allowed to touch `all_rows.html`

Every scan script (`megascan.py`, `megascan_yahoo.py`, `insider_scan.py`, `scan_values.py`, `fundamentals_scan.py`) writes only to its own independent raw data file, then calls `python build_site.py` once at its own end - it runs all 9 `merge_*.py` scripts sequentially in one process (never concurrently) and reassembles `nasdaq-stocks.html`, with its own file lock so two scans finishing near-simultaneously serialize instead of racing. **This exists because running scans concurrently (which SCAN ALL and the site's "Run All Background" button both do on purpose, to save time) used to cause a lost-update race on the shared `all_rows.html` - see `build_site.py`'s own docstring for the full story.** If you ever add a new scan script or a new `merge_*.py`, do NOT have the scan script reassemble the site itself - write your raw data file, add the new merge script to `build_site.py`'s `MERGE_SCRIPTS` list, and call `build_site.py` like every other scan does.

## Code name `SCAN ALL` (added 2026-09-05) — runs everything together

**Trigger phrase**: "SCAN ALL". Runs all 4 named refresh routines in this file. **Every time SCAN ALL is invoked, ask the user first whether to include `SCAN RED`** in this run (it alone adds ~2h to the ~1h the rest takes) - do not assume a default, always ask (this was the user's explicit correction 2026-09-05 after initially agreeing to "always include").

1. **Ask the user**: include `SCAN RED` this time, or skip it and just do MEGASCAN + MEGASCAN YAHOO + SCAN HOLDINGS?
2. **Launch `MEGASCAN`, `MEGASCAN YAHOO`, and `FUNDAMENTALS SCAN` together in the background** (`python megascan.py`, `python megascan_yahoo.py`, `python fundamentals_scan.py`) - all three are standalone scriptable jobs hitting different domains/endpoints, safe to run concurrently, no shared rate-limit risk (FUNDAMENTALS SCAN is pure HTTP against Yahoo's quoteSummary/chart APIs, ~2-3 min for the full universe - much faster than the other two). Back up `analyst_targets_*.txt` / `yahoo_targets_*.txt` / `yahoo_dividends_*.txt` first if not already done recently.
3. **While the background scans run, do `SCAN LIVE` (see below)** - covers `SCAN HOLDINGS` + `SCAN EXITS`, and `SCAN RED` too if the user opted in at step 1.
4. **Report a single combined summary** at the end: MEGASCAN new-green/lost-coverage counts, MEGASCAN YAHOO updated/no-data counts, FUNDAMENTALS SCAN updated/no-data counts, plus SCAN LIVE's own combined summary (see below) - not five separate reports scattered through the conversation.

## Code name `SCAN LIVE` (added 2026-09-10) — bundles every scan that needs a live Claude session

**Trigger phrase**: "SCAN LIVE" (or "תעשה סריקה חיה" / "תעדכן הכל בעטורו"). Runs the three scans that are marked 🧠 "דורש קלוד חי" on the site (`SCAN HOLDINGS`, `SCAN EXITS`, `SCAN RED`) back to back in one pass, instead of asking for each separately - all three need the exact same thing (a live `mcp__claude-in-chrome__*` session on the user's real, logged-in eToro tabs), so there's no reason not to just do all three once that session is open.

**Not the same thing as `SCAN ALL`**: `SCAN ALL` also launches the three standalone/scriptable cloud-style scans (MEGASCAN, MEGASCAN YAHOO, FUNDAMENTALS SCAN) in the background - `SCAN LIVE` is only the live-session trio, useful on its own when the user just wants the eToro-account-specific data refreshed without touching the (usually cloud-automated) analyst-coverage data at all.

**Order** (fastest/most-likely-to-matter first, slowest/optional last):
1. **Ask the user**: include `SCAN RED` this time? (adds ~2h for ~250 tickers at 25-30s/ticker pacing - same ask as `SCAN ALL` step 1, don't assume a default).
2. **`SCAN HOLDINGS`** - checks both Real and Virtual for new/filled/closed positions and pending orders (see its own section below for the full procedure). Auto-chains `SCAN VALUES` at its own end.
3. **`SCAN EXITS`** (code name `SCAN EXIT HISTORY` below) - same eToro session, so do it right after HOLDINGS while already logged in and on the account. Checks `scan_checkpoint.json` first (or run `python update_exit_history.py` with no arguments) to see exactly which date each account was last scanned to, then only scrolls/transcribes exits newer than that checkpoint instead of the whole history - the once-manual "scroll to the very start" pass from before 2026-09-10 is no longer needed on repeat runs.
4. **`SCAN RED`**, only if opted into at step 1 - re-verifies the current Not Tradeable list against eToro itself.
5. **Report one combined summary**: SCAN HOLDINGS structural changes (new/closed positions, pending orders, TP changes), SCAN EXITS new profitable exits found + updated Re-entry Watchlist candidate count, SCAN RED bugs found (if run).

## `FUNDAMENTALS SCAN` (added 2026-09-05) — feeds the Score/Short Interest/RSI/P&E columns

`python fundamentals_scan.py` - pure HTTP (no browser), hits Yahoo Finance's `quoteSummary` (needs a crumb+cookie handshake done once at startup, see the script's own comments) and `chart` endpoints for every ticker. Writes `fundamentals_data.tsv`, then chains into `merge_fundamentals.py` (Short Interest %/RSI/P-E cells) and `compute_score.py` → `score_history.py` → `merge_score.py` (the composite Score column, its daily history snapshot, then the site merge) automatically at the end - running it alone is enough to refresh all 4 of those columns, no separate steps needed. ~2-3 min for the full 6,356-ticker universe. If a re-run reports "0 rows tagged" from the merge step, check `fundamentals_data.tsv`'s actual field count against what the merge script's parser expects before assuming the scan itself failed (this exact bug happened once - a stale `!= 7` check on an 8-field line).

## `Hedge Funds` column (added 2026-09-06) — free addition from MEGASCAN's own page

Same TipRanks page MEGASCAN already fetches has a "HEDGE FUND ACTIVITIES" table (the top ~3 default-visible holders, e.g. Warren Buffett/Berkshire) showing each fund's latest quarterly action (Added/Reduced/No change/New Position/Sold Out). `parse_hedge_fund_activity()` in `megascan.py` extracts this at zero extra network cost, writes `hedge_fund_activity.tsv` (TICKER, added, reduced, unchanged, total), and `merge_hedgefund.py` (added to `build_site.py`'s sequence) renders it as an "A/R/N" label, color-graded but deliberately **not** part of the Score total - sample size is only the ~3 default-shown holders, not the full list, so it's informal context (like P/E), not a scored signal.

## Six more columns + a Secondary Score (added 2026-09-06, all from `fundamentals_scan.py`/`megascan.py`'s already-fetched pages)

- **Beta**, **PEG**, **52W Range** - all three come from the same Yahoo `quoteSummary` call `fundamentals_scan.py` already makes for Short%/P-E/Market Cap (`defaultKeyStatistics.pegRatio`, `summaryDetail.beta`/`fiftyTwoWeekHigh`/`fiftyTwoWeekLow`) - zero extra network cost. None of the three feed the main Score (Beta and 52W Range have no universal good/bad direction at all; PEG does but is scored into the **Secondary Score** instead, see below).
- **Volume Spike** - `fundamentals_scan.py`'s existing Yahoo `chart` call already returns a `volume` array alongside `close`; computes today's volume ÷ trailing-30-day average, paired with the same-day price change to give it direction (a spike means nothing on its own - it needs the price move to say whether it's bullish or bearish).
- **Hedge Fund Activity** - from `megascan.py`'s TipRanks page (see the section above) - Added/Reduced/No-change among the top ~3 default-shown holders.
- **`compute_secondary_score.py`** (chained after `compute_score.py`, before `build_site.py`) - a SEPARATE 0-10 score built only from PEG (falls back to raw P/E if PEG unavailable), Hedge Fund Activity, and Volume Spike - the three metrics above that were deliberately excluded from the main Score. Kept as its own column (with its own `X/3` confidence indicator and its own pair of range filters, mirroring the main Score's UI exactly) rather than blended into the main Score, specifically so neither score's meaning gets diluted - see the column's own tooltip for the full reasoning.
- **`compute_risk_score.py`** (chained after `compute_secondary_score.py`) - a THIRD score, different in *kind*: not quality (bullish/bearish) but volatility/instability (calm/wild), from Beta, distance from the 52W Range midpoint, and Volume Spike magnitude alone (no price direction) - three metrics with zero bullish/bearish direction individually, but a shared "volatility" theme. Colored blue/gray/orange, deliberately not green/red, so "high" never visually reads as "bad".

## Yahoo exchange-suffix mismatch fix + 2 more scoring signals per score (added 2026-09-06)

**"No data" ticker fix**: `fundamentals_scan.py`'s "no data" count was 839/6356 (13%) - investigated and found almost all of them share one root cause, not 839 individual failures: eToro's exchange suffix convention doesn't match Yahoo Finance's own (`.ASX` vs Yahoo's `.AX`, 5-digit `.HK` codes vs Yahoo's 4-digit, `.ZU` vs `.SW`, `.NV` vs `.AS`, Stockholm `.ST` share-class tickers needing a hyphen like `WALLb`→`WALL-B`). Worse, a malformed symbol often still gets an HTTP 200 from Yahoo's chart endpoint with a `result` shell but null close prices, not a clean 404 - `resolve_yahoo_symbol()` in `fundamentals_scan.py` checks for an actual non-null close price, not just a 200 status, before trusting a candidate symbol. Only probes alternate symbols for tickers whose suffix is a known mismatch (adds one extra lightweight `chart` call for those only, not all 6356). Cut "no data" from 839 to ~204 (mostly genuine cases: delisted/moved-exchange tickers like `TKWY.NV`, and exchanges Yahoo doesn't cover at all like Abu Dhabi's `.DH`).

**2 new signals added to each of the 3 scores** (all piggyback on the same Yahoo `quoteSummary` call already being made, via 3 more modules: `financialData`, `earningsHistory`, `earningsTrend` - zero extra requests):
- **Score** (5→7 signals, confidence now `X/7`): added **Analyst Dispersion** (Low-High target spread relative to Avg - tight spread = analysts agree = bullish-leaning) and **Earnings Surprise** (avg beat/miss % over the last few reported quarters from Yahoo's `earningsHistory`).
- **Secondary Score** (3→4 signals, confidence now `X/4`, scale now `raw*10/8`): added **EPS Trend** (whether analysts raised or cut this quarter's EPS estimate over the last 90 days, from `earningsTrend` - a leading indicator that often moves before the Rating itself).
- **Risk Score** (3→5 signals, confidence now `X/5`, no scaling needed since 5×2=10 already): added **Debt/Equity** (`financialData.debtToEquity` - balance-sheet leverage/fragility) and **Days-to-Cover** (`defaultKeyStatistics.shortRatio` - short-squeeze risk, high value means shorts could be forced to cover and move price sharply either way).

All 4 new raw fields (`debt_to_equity`, `short_ratio`, `earnings_surprise_avg`, `eps_trend_pct`) were added to the end of `fundamentals_data.tsv` (14→18 fields) as score inputs only, no new visible table columns - every reader of that file (`compute_score.py`, `compute_secondary_score.py`, `compute_risk_score.py`, `merge_fundamentals.py`, `update_price.py`, `score_history.py`) had its `len(parts) != N` check updated to 18 in the same pass, along with every downstream `score.tsv`/`secondary_score.tsv`/`risk_score.tsv` field count and the on-site tooltips/range-filter JS (`part1_fixed.html`/`part3.html`) for the new `X/7`/`X/4`/`X/5` confidence denominators - this file-schema-change has bitten this project before (see the project memory's "field-count check footgun" entry), so every reader was audited via `grep -rn "len(parts) !="` in the same session rather than fixed incrementally.

## Round 2 (2026-09-06, same day): 3 more scoring signals + Overall Score + daily automation

**3 more free signals** (same pattern as round 1 - piggyback on the existing `quoteSummary` call, one more module `recommendationTrend`, zero extra requests):
- **Score** (7→8 signals, confidence now `X/8`): added **Rating Trend** - the change in analysts' average recommendation (1=Strong Sell..5=Strong Buy) over the last 3 months, from `recommendationTrend`'s `0m`/`-3m` periods. Catches upgrade/downgrade momentum a static Rating snapshot can't show (a "Hold" looks identical whether just downgraded from Buy or upgraded from Sell).
- **Secondary Score** (4→6 signals, confidence now `X/6`, scale now `raw*10/12`): added **Profit Margin** and **Revenue Growth**, both from `financialData` (`profitMargins`, `revenueGrowth` - raw values are fractions, e.g. 0.276 = 27.6%).

**More exchange-suffix fixes** in `yahoo_symbol_candidates()`: `.EUR`/`.24-7` (eToro's alternate-currency/24-hour-venue listings of ordinary US stocks like `AAPL.EUR`, `AMZN.24-7` - not separately listed on Yahoo, bare ticker is the fix) and `.CO` (Danish share-classes need the same hyphen-insertion trick as `.ST`, e.g. `AMBUB.CO`→`AMBU-B.CO`).

**New: Overall Score column** (`compute_overall_score.py`/`merge_overall_score.py`) - a single blended number = `Score×0.7 + SecondaryScore×0.3`, for anyone who wants one number instead of two. Deliberately **excludes Risk Score** (volatility axis, not quality - blending it in would make the result meaningless, consistent with why Risk Score was kept separate from day one). Confidence is the SUM of both scores' own confidence counts (not an independent measurement) - `X/14` (8 from Score + 6 from Secondary). Added to `build_site.py`'s `MERGE_SCRIPTS` (after `merge_risk_score.py`) and `fundamentals_scan.py`'s chain (after `compute_risk_score.py`, before `score_history.py`) - runs automatically, no manual step.

**Daily automation**: a Windows Task Scheduler task named `"eToro FUNDAMENTALS SCAN"` runs `python fundamentals_scan.py` every day at 06:00 (working directory set to the project root, so all the script's relative-path reads/writes and its own subprocess chain work exactly as when run manually) - refreshes Score/Secondary Score/Risk Score/Overall Score and every fundamentals column without anyone needing to trigger it. Manage it with `Get-ScheduledTask -TaskName "eToro FUNDAMENTALS SCAN"`, `Disable-ScheduledTask`, or `Unregister-ScheduledTask` in PowerShell, or via the Windows Task Scheduler GUI (`taskschd.msc`). This does NOT run MEGASCAN/MEGASCAN YAHOO/SCAN HOLDINGS/SCAN RED - those either need a live browser session or weren't asked to be automated; `fundamentals_scan.py` was chosen because it's a pure-HTTP standalone script that alone already refreshes 4+ scores/columns.

All the same field-count/tooltip/range-filter update discipline from round 1 applied again: `fundamentals_data.tsv` grew 18→21 fields, every reader's `len(parts) != N` check updated, every on-site tooltip/slider/JS fallback for the new `X/8`/`X/6`/`X/14` confidence denominators updated in `part1_fixed.html`/`part3.html`.

## Round 3 (2026-09-06, same day): sector percentile, sparkline trend, meaningful-change flag

User asked "how can we improve more?" a third time; this round is bigger/structural rather than "one more free signal," per the user's own framing when picking the direction.

**Sector data**: `fundamentals_scan.py` now also fetches the `assetProfile` module (adds `sector`/`industry` - e.g. "Technology"/"Consumer Electronics" for AAPL) and writes it to its OWN file, `sector_data.tsv` (TICKER, sector, industry), deliberately NOT appended to `fundamentals_data.tsv` - two categorical strings that no score formula uses as a number didn't need to grow that file's field count (and every one of its 7 readers) a third time.

**Sector Percentile column** (`compute_score_percentile.py`/`merge_score_percentile.py`, new `col-percentile`/`sortPercentile`): ranks each ticker's Overall Score against only its own sector's peers (0-100%, e.g. "78%" = beats or ties 78% of same-sector tickers) - a raw Overall Score of 7 means something different in Technology (usually high scorers) vs Utilities. Only computed for sectors with 5+ tickers (`MIN_SECTOR_SIZE` in the script) - below that, a percentile is close to meaningless since one company can swing it from 0 to 100 alone. Added to `add_score_column.py`'s migration chain (after `overallscore-cell`) and `build_site.py`'s `MERGE_SCRIPTS` (after `merge_overall_score.py`).

**Inline sparkline + meaningful-change badge, both decorate the Overall Score cell itself** (not separate columns - they're visualizations OF that score, not new independent data):
- `compute_score_change.py` (new, chained after `score_history.py` since it needs today's row already appended) compares each ticker's Overall Score between the two most recent DISTINCT dates in `score_history.tsv`, writes `score_change.tsv` only for moves >= `THRESHOLD` (1.0 point on the 0-10 scale) - small day-to-day noise is deliberately not flagged. **Produces an empty file until there are 2+ distinct days of history** - this is expected on the day it was built (only "today" exists) and will start populating from the Task Scheduler's next 06:00 run onward, not a bug to chase.
- `merge_overall_score.py` was extended (not a new script - all three concerns share one cell) to also read `score_change.tsv` (renders a ▲/▼ badge, color-coded, with an exact-delta tooltip) and `score_history.tsv` directly (takes each ticker's last 14 distinct days' Overall Score, writes them as a `data-overallscore-history="6.9,6.8,7.0,..."` attribute on the `<tr>`) - `part3.html`'s new `renderSparklines()` (runs once on page load, not on every filter/sort since history doesn't change until the next day's scan) reads that attribute and draws a small inline SVG trend line into a `<span class="oscore-spark">` placeholder inside the cell.

All three wired into `fundamentals_scan.py`'s chain in dependency order: `compute_overall_score.py` → `compute_score_percentile.py` → `score_history.py` → `compute_score_change.py` → `build_site.py`.

## Filter accordion (2026-09-07) — collapsed the 10 range-filter bars into 6 groups

User asked for less clutter: the range-filter bars (Upside%, TP/Yahoo Ratio, Score, Secondary Score, Risk Score, Overall Score - 10 bars total once each score's value+confidence pair is counted) used to all render open, flat, one after another, taking a lot of vertical space even when most weren't in use. Restructured `part1_fixed.html` into a `<div class="filter-accordion">` of 6 native `<details class="filter-group" name="filterAccordionGroup">` elements (Upside%, TP/Yahoo Ratio, Score, Secondary Score, Risk Score, Overall Score) - the shared `name` attribute makes them a mutually-exclusive accordion in browsers that support it (opening one auto-closes another), with graceful degradation elsewhere. Each group's original filter-bar `<div id="...RangeFilter">` markup (IDs untouched) now lives inside a `.filter-group-body` wrapper, so **no part3.html filter LOGIC needed to change** - only the DOM nesting around it.

Since a collapsed filter can silently keep narrowing the table without being visible, added a small dot indicator (`.filter-group-dot`) on each group's `<summary>` header, lit via a new `updateFilterGroupDots()` in `part3.html` (called at the top of `applyFilters()`, so it stays in sync automatically) - compares each range's current min/max against its true default (dynamic for Upside%'s min/max, static for the rest) and toggles a `.filter-active` class on the `<details>` element. This is the safety net that makes collapsing sane: a user can tell at a glance which categories are actively filtering even with their bars hidden.

## `portfolio_server.py` now auto-starts on Windows login (2026-09-07)

The site's actual backend - `portfolio_server.py`, the local HTTP server that serves `nasdaq-stocks.html` AND handles the scan buttons' `POST /run/<name>` + `GET /status` polling - was previously only ever started manually (`python portfolio_server.py`). A plain `python -m http.server` (no `/status`/`/run/*` support, just static files) was mistakenly used for local preview at one point - if the scan buttons don't respond and the browser console shows repeated 404s on `/status`, that's the tell that the WRONG server is running; `.claude/launch.json`'s `static-site` config now correctly points at `portfolio_server.py`, not `http.server`.

**Auto-start on login**: `C:\Users\T\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\etoro_site_server.vbs` launches `portfolio_server.py` silently (hidden window) every time this Windows account logs in - covers both "restart the computer" and "open the workspace later" without the user ever running the server by hand. **Why the Startup folder, not Task Scheduler**: tried `Register-ScheduledTask` with an `AtLogOn` trigger first (matching the existing "eToro FUNDAMENTALS SCAN" daily task's pattern) - failed with "Access is denied" for this non-admin Windows account specifically for logon-triggered tasks (time-based triggers like Daily work fine for this account; logon triggers are blocked by this machine's policy). The Startup folder is the standard no-admin-required workaround and needs no elevation.

**Encoding gotcha worth remembering**: the VBS file's command string contains the project's Hebrew path (`H:\קלוד\קלוד 2 - Copy\...`) - writing it as plain UTF-8 (the default for most file-write tools) silently breaks it, because `wscript.exe` expects VBScript source in the system codepage or **UTF-16LE with a BOM** for Unicode literals to parse correctly; a UTF-8 Hebrew path gets mis-decoded into garbage, so `python.exe` receives a broken path argument and exits immediately with no visible error (the launch *looks* like it worked - `wscript.exe` returns fine - but no server ever binds to the port). Fixed via `[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::Unicode)` in PowerShell. If this `.vbs` file is ever edited again, it must be re-saved the same way, not with a plain text editor defaulting to UTF-8.

## Round 4 (2026-09-07): 3 more Score signals - ROE, Institutional Ownership, Current Ratio

User asked to add these directly to the main Score (not Secondary/Risk) - Score grows 8→11 signals, confidence now `X/11`. All 3 come from Yahoo modules already fetched (`financialData`/`defaultKeyStatistics`), zero extra requests:

- **ROE** (`financialData.returnOnEquity`, raw fraction e.g. 1.4875 = 148.75%) - profitability efficiency, >25%=2pts, negative=0pts.
- **Institutional Ownership** (`defaultKeyStatistics.heldPercentInstitutions`) - rough "smart money" confidence signal, >70%=2pts, <10%=0pts.
- **Current Ratio** (`financialData.currentRatio`) - short-term liquidity, but a SWEET SPOT unlike the other 10 signals: <1.0=0pts (liquidity risk), 1.5-3.0=2pts (healthy), >3.0=1pts (idle cash, not necessarily great) - the only Score signal with this non-monotonic shape.

`fundamentals_data.tsv` grew 21→24 fields (same footgun discipline as every prior round - all 6 readers' `len(parts) != N` checks updated via one `sed` pass, verified with a grep afterward). Score's raw-total denominator changed 16→22 (11 signals × max 2pts); **this also changed Overall Score's confidence denominator** (8+6=14 → 11+6=17) since Overall Score sums Score's and Secondary Score's confidence counts directly - every `/14` reference (tooltips, range-filter bounds/JS, `merge_overall_score.py`'s confidence_class thresholds) had to be hunted down and changed to `/17` alongside the more obvious `/8`→`/11` ones. This is worth remembering as its own pattern: **changing one score's signal count can silently invalidate a DIFFERENT score's confidence scale if that second score derives its confidence by summing the first one's** - Overall Score is the only case of this in the codebase so far, but if a future score ever composites another score's confidence again, audit for stale `/N` literals the same way.

## `update_price.py` (added 2026-09-06) — closes the "Price never refreshes" gap

`python update_price.py` (chained automatically after `merge_fundamentals.py` inside `fundamentals_scan.py` - never needs to be run by hand). Writes `fundamentals_data.tsv`'s Yahoo chart close price back into `analyst_targets_*.txt`'s price field, then re-runs `merge_analyst_targets.py`. **Context**: Price was static since the site's original construction - no scan (MEGASCAN, SCAN VALUES) ever touched it, they only ever wrote Low/Avg/High and left price untouched. `fundamentals_scan.py` was already fetching a fresh Yahoo close price per ticker for its own RSI/MA math but never wrote it anywhere visible - this closes that gap with data already being fetched, no new network calls.

## `score_history.py` (added 2026-09-06) — daily Score snapshots for future forward-testing

Appends one row per ticker (`DATE, TICKER, SCORE, CONFIDENCE, PRICE`) to `score_history.tsv` every time `compute_score.py` runs (chained automatically - never needs to be run by hand). Idempotent per day: re-running on the same date replaces that date's rows rather than duplicating them, so running FUNDAMENTALS SCAN twice in one day is harmless. **Why this exists**: a real backtest of the Score formula needs point-in-time historical values for its inputs (Rating, Insider $, Short Interest%, etc.), and none of the free sources expose those retroactively - only current state. So instead of backtesting the past, this is building the data for a **forward test**: once a few months of daily snapshots accumulate, a future session can join `score_history.tsv` against later price data and check whether tickers that scored high on day X actually outperformed low-scorers by day X+30/X+90. Don't expect to run any real analysis on this file for a while - it needs time to accumulate, not more code.

Steps 3-4 must be sequential (both need the same live browser session); step 2 can safely overlap with 3-4 since they're independent background processes touching different files.

**Read this file at the start of any session that touches analyst price targets.** It documents the cheapest, safest, reusable method for refreshing eToro/TipRanks analyst data (Low/Avg/High), discovered and validated 2026-08-31 during the NOFAQ audit.

## Why this method exists

The user asked to refresh all 4,330 tickers that are currently TRADEABLE + have real TipRanks coverage (`OK` status), since their Low/Avg/High values were scraped at different times over many sessions and go stale. Going forward this should happen **roughly daily**.

## The method (safe, cheap, no eToro login/block risk)

Navigate directly to TipRanks' own public widget page — this is the EXACT same widget eToro embeds via iframe on its own `/markets/{ticker}/research` page, just accessed at the source instead of through eToro's wrapper:

```
https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light
```

- No login required, not eToro's domain, **no Cloudflare/rate-limit risk observed** (unlike eToro's own site, which has blocked us before — see `NOT_TRADEABLE_AUDIT_LOG.md`).
- Confirmed identical data to what eToro's own page shows.
- **Only gives analyst coverage data (Low/Avg/High, consensus)** — does NOT give live price or tradeability (Trade button state). For those two, eToro's own page is still required (with the slow, careful, login-verified protocol documented in `NOT_TRADEABLE_AUDIT_LOG.md`).

### Critical caveat — ticker suffix stripping

Tickers with `.US`, `.A`, `.B`, `.EUR`, or `/V` suffixes (internal site disambiguators, not real TipRanks identifiers) **silently return "no data" on this widget even when real coverage exists**. Always strip these suffixes before querying, and keep the ORIGINAL suffixed form as the output key (so it matches the site's own ticker convention). Real exchange suffixes (`.L`, `.DE`, `.PA`, `.HK`, `.T`, `.ST`, `.BR`, `.HE`, `.CO`, `.AS`, `.MI`, `.MC`, `.OL`, etc.) are NOT affected — query those as-is.

### Extraction snippet

```js
const t = document.body.innerText;
const idx = t.indexOf('LOW ESTIMATE');
t.slice(idx - 30, idx + 80)
```
or for a broader read:
```js
const t = document.body.innerText;
const idx = t.indexOf('ANALYST PRICE TARGET');
document.title + ' ||| ' + (idx >= 0 ? t.slice(idx, idx + 350) : 'NOSECTION')
```

Pattern: `{Low} LOW ESTIMATE {Avg} AVERAGE PRICE TARGET {High} HIGH ESTIMATE`.

**Edge case**: some tickers show individual analyst ratings (Buy/Sell/Hold + a price each) WITHOUT an aggregated LOW/AVERAGE/HIGH box. When this happens, compute Low=min, Avg=mean, High=max of the listed individual analyst targets — same convention used throughout this project's history for "widget-format variant" cases (see `OSLO_LETTER_STATUS.md` for precedent).

**"This stock has no research data"** (or no ANALYST PRICE TARGET section at all) = genuinely no coverage, record NOFAQ.

## Pacing

The user has explicitly asked for a deliberate, non-robotic pace: **15-20 seconds per ticker, varied (not a fixed constant)**. Since this domain has shown no block risk so far, running multiple PARALLEL agents is fine (unlike eToro, where parallel workers would multiply the risk of the shared IP getting rate-limited) — but each individual worker should still pace itself slowly and deliberately, per the user's standing preference, not because of a known technical constraint on this domain.

## Chunking / parallelization pattern

For a full-dataset refresh (thousands of tickers):
1. Extract the target ticker list from the live site (`nasdaq-stocks.html`) into a `.tsv` (ticker + exchange columns) — filter by whatever subset needs refreshing (e.g. all `OK`+`TRADEABLE` rows).
2. Split into ~400-ticker chunks (empirically, one agent session can reliably get through ~400-450 tickers at the 15-20s pace before running out of budget).
3. Launch one background `Agent` per chunk, each writing to its own `REFRESH_LOG_<N>.md` to avoid write-conflicts, each getting its OWN Chrome tab (`tabs_create_mcp`) and never touching other tabs in the shared group.
4. Each agent updates its assigned tickers' source `analyst_targets_*.txt` file directly as it goes (or logs new values for a later consolidation pass — either is fine, but updating directly is simpler for a routine refresh since there's no "verify vs fix" split like the audits had).
5. After all chunks finish: re-run `merge_analyst_targets.py`, reassemble `nasdaq-stocks.html` (`cat part1_fixed.html all_rows.html part3.html > nasdaq-stocks.html`), verify row counts, send to user.

## Known related files

- `NOT_TRADEABLE_AUDIT_LOG.md` — the eToro-side audit (tradeability), found 73/321 false negatives, fixed.
- `NOFAQ_AUDIT_LOG.md` (+ `NOFAQ_AUDIT_LOG_1.md` through `_6.md`) — the TipRanks-widget-side audit (coverage), found 230/2413 false negatives, fixed.
- `refresh_4330_list.tsv` — the list of currently-confirmed OK+TRADEABLE tickers, extracted 2026-08-31, used as the seed list for the first full refresh pass.
- Analyst data lives in per-letter/per-exchange `analyst_targets_*.txt` files (format: `TICKER\tName\tPrice\tLow\tAvg\tHigh\tAnalysisStatus\tTradeStatus`, tab-separated). Files with `_OLD` in the name are excluded from the merge (`merge_analyst_targets.py` globs `analyst_targets_*.txt` and skips any containing `_OLD`).

## New: Yahoo Dividend Yield column (added 2026-08-31)

Added a new "Div Yield" column to the Yahoo Finance section of the table (separate from eToro's own existing "Div. Yield" column), per user request — a distinct, independently-sourced dividend figure for comparison.

**Source**: Yahoo Finance's own quote page (`https://finance.yahoo.com/quote/{TICKER}`), NOT the TipRanks widget (TipRanks does not show dividend data at all). Extract via:
```js
const t = document.body.innerText;
const idx = t.indexOf('Forward Dividend & Yield');
t.slice(idx, idx+80)
```
Pattern: `Forward Dividend & Yield\n{amount} ({percent}%)`. Store just the percent number (e.g. `0.34`) — the `%` sign is added at display time by the site's JS.

**Template changes made** (for future reference, so nobody re-derives this):
- `part1_fixed.html`: new `<th id="sortYhDiv">` between High and Upside % in the Yahoo header group; colspan bumped 7→8; added `.yh-div` to the shared CSS color rules alongside `.yh-low/.yh-avg/.yh-high`.
- `part3.html`: added `'div'` to `updateYahooColumns()`'s field list (with special `+ '%'` formatting since, unlike Low/Avg/High, this isn't a currency value); added `sortYhDiv` wiring (variable, `sortThs` map, `numericKeys` array, click listener, source-highlight toggle array) — same pattern as every other Yahoo column.
- `add_yahoo_div_column.py`: one-time migration script that inserted the new `<td class="yh-div col-yahoo empty">` placeholder cell into all existing rows in `all_rows.html` (idempotent — safe to re-run).
- `merge_yahoo_dividends.py`: new merge script (mirrors `merge_yahoo_targets.py`) that reads `yahoo_dividends_*.txt` files (format: `TICKER<TAB>DividendPercent`, e.g. `AAPL\t0.34`) and injects `data-yh-div="X"` onto each `<tr>`.

**Output file naming**: `yahoo_dividends_<chunk-or-exchange>.txt`, same tab-separated convention as everything else in this project.

Scope of the first pass: the 4,330 tickers in `refresh_4330_list.tsv` (the currently-confirmed TRADEABLE+OK set) — not the full 6,761, since NOFAQ/not-tradeable tickers weren't the focus of this request.

## New: "Scan Portfolio" button — local Playwright server (added 2026-09-01)

Per user request: a button on the site that scans ONLY the portfolio holdings (not the whole exchange) on demand — e.g. right after buying/selling a stock — using a fully local, LLM-free pipeline (fast, free, no Claude session needed).

**Why this works without me (Claude) in the loop each time**: verified both TipRanks widget and Yahoo Finance render their data via client-side JavaScript (confirmed via `curl` — raw HTML has none of the target text), so a plain HTTP scraper won't work, BUT a local **headless Chromium via Playwright** does — same rendering, zero LLM cost, and much faster than the 15-20s/ticker human-paced protocol used elsewhere in this project (that pacing was a discretionary safety choice for eToro specifically, not a technical requirement for TipRanks/Yahoo).

**Files**:
- `portfolio_server.py` — the whole thing: serves the site (replaces `python -m http.server` for local dev) AND handles `POST /scan-portfolio`. Reads HELD tickers from `portfolio_virtual.tsv` + `portfolio_real.tsv`, scrapes each via Playwright (TipRanks for Low/Avg/High, Yahoo for dividend), updates the relevant `analyst_targets_*.txt` files + `yahoo_dividends_PORTFOLIO.txt` in place, re-runs both merge scripts, reassembles `nasdaq-stocks.html`, returns a JSON summary.
- `start_portfolio_server.bat` — double-click launcher (Windows), just runs `python portfolio_server.py`.
- Button added to `part1_fixed.html` (`#scanPortfolioBtn`, next to the Account toggle) + JS wiring in `part3.html` (`fetch('/scan-portfolio', {method:'POST'})`, then reloads the page on success).

**Known gotcha discovered and fixed during setup**: a fresh (cookie-less) Playwright browser hits Yahoo's GDPR/cookie consent wall on first navigation (geolocation-dependent — appeared in Hebrew for this IP, "העדפות הפרטיות שלך"), which blocks ALL page content, including the dividend figure, until dismissed. `dismiss_yahoo_consent()` handles this once per browser launch (tries both Hebrew and English button text), then re-navigates. Also: `wait_until="networkidle"` was unreliable/timed out on both TipRanks and Yahoo (same lesson learned repeatedly throughout this whole project with the browser-automation agents) — switched to `wait_until="domcontentloaded"` + an explicit `wait_for_timeout()`.

**Scope, deliberately narrow per user's explicit request**: portfolio only (currently 55 tickers), NOT a replacement for the full-exchange refresh infrastructure documented earlier in this file. Those are two separate, independently-useful tools — don't conflate them or try to point this button at the full 4,330/6,761-ticker set.

**To run**: double-click `start_portfolio_server.bat` (or `python portfolio_server.py`), then open `http://localhost:8791/nasdaq-stocks.html` — note this is a DIFFERENT way of opening the site than the plain `file://` path or the plain static-file server; the Scan Portfolio button only works when reached through this custom server (it needs the `/scan-portfolio` endpoint, which a plain file:// page or `python -m http.server` doesn't have).

## "Scan eToro" / code name SCAN HOLDINGS — real account/portfolio check (added 2026-09-01, named 2026-09-05)

**Code name: `SCAN HOLDINGS`.** Trigger phrases the user may use: "סרוק eToro", "scan eToro", "scan portfolio", "תסרוק פורטופוליו", or the code name itself — one command that tells the user everything going on in their account (new positions, filled/closed positions, pending orders), for both Real and Virtual. If ambiguous whether they mean this or `SCAN VALUES` (the analyst-data-only button), ask which one they mean.

**Auto-chains into SCAN VALUES at the end (added 2026-09-05, user-requested)**: after finishing the structural reconciliation (step 9 below) and reassembling the site, automatically trigger the `/scan-portfolio` endpoint on `portfolio_server.py` (same effect as clicking the "Scan Portfolio" button, i.e. running `SCAN VALUES`) so any newly-filled/newly-added HELD position gets a fresh analyst Low/Avg/High + dividend yield immediately, without the user having to ask separately or click the button themselves. Requires `portfolio_server.py` to be running (`http://localhost:8791`) — start it first if it isn't. This only makes sense to run once per SCAN HOLDINGS pass (it refreshes ALL held tickers each time, not just the changed ones — cheap enough, ~1-2 min for 55 tickers, that this is fine).

**What this actually checks** (different from the button above): the user's real eToro account state — open positions, units, avg open price, P/L, Take Profit (TP), Stop Loss (SL), and pending orders that haven't filled yet. This is portfolio MANAGEMENT data, not analyst research data.

**Why this can't be a fully automated button**: requires the user's real logged-in eToro session. The login/session cookie is HttpOnly (not readable via page JS), and even if it were extractable, saving a live session token to a local file would be a real security exposure (real money account). So this must be run by Claude directly through the `mcp__claude-in-chrome__*` tools (the user's actual logged-in Chrome), not handed off to an unattended local script. The user has explicitly chosen this tradeoff (manual trigger, ask Claude each time) over the security risk.

### Procedure

1. Get/create a tab via `tabs_create_mcp`, navigate to `https://www.etoro.com/portfolio` (redirects to `/portfolio/overview`).
2. Click the **"Manual Trades"** tab (NOT the default view, which may land on whatever tab was last selected — Angular SPA persists tab state). Click via `javascript_tool` finding the button by text (`Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Manual Trades')`) rather than pixel coordinates — the account/portfolio page has a **viewport-vs-screenshot scale mismatch** (e.g. real viewport 1894×731 vs a 1568×605 screenshot), so coordinate-based clicks land in the wrong place. Always resolve elements by text/ref, not screenshot pixel coordinates, on this page.
3. **The holdings table is virtualized** (only ~46-50 of e.g. 54 rows render initially, even after scrolling the page or setting `scrollTop` programmatically on the scroll container `.et-layout-scrollable-page` — that does NOT trigger the framework's render-more-rows logic). What DOES work: a **real synthetic mouse-wheel scroll** via `computer{action:"scroll", coordinate:[x,y], scroll_direction:"down", scroll_amount:10, repeat:15}` (or several calls) over the table area. Verify full coverage by counting `(document.body.innerText.match(/^Buy$/gm)||[]).length` against the "Asset (N)" header count before trusting the capture.
4. Extract via `document.body.innerText` (or `get_page_text`) — format is a repeating block per position:
   ```
   Buy
   TICKER
   [optional "24/5" label — ignore, it's a leverage/CFD-availability badge, not part of the ticker]
   DDMMYYYYHHmm  (date+time squashed together, no separator)
   UNITS
   OPEN_PRICE
   SL  (or "----" if none set)
   TP  (or "----" if none set)
   DAILY_P/L
   P/L
   P/L%
   Sell
   ```
   Some tickers appear as **multiple separate entries** (different open dates = separate lots, e.g. two WMT rows, two WYNN rows) — the site's per-ticker table can only show one row per ticker, so when writing back to `portfolio_*.tsv` a duplicate ticker will just overwrite to the last-seen lot (a known, accepted modeling limitation, not a bug to fix).
5. Click the **"Orders"** tab too (same page, same button-by-text pattern) — shows pending orders not yet filled (status "Received" etc.), with columns Asset/Current/Invested/Execute At/SL/TP/Status/Leverage. If empty, it says "There are no pending orders" — this itself is useful information (report it).
6. **Switch accounts** to check both: click the account-switcher pill (top-left, shows "Virtual Portfolio / Demo" or "Main Account / Real" — find via `Array.from(document.querySelectorAll('button, [role="button"]')).find(b => /Main Account|Virtual Portfolio/i.test(b.textContent))`) and repeat steps 2-5 for the other account. Don't forget to re-click "Manual Trades" after switching — the tab selection can reset.
7. Compare the freshly parsed data against the stored `portfolio_virtual.tsv` / `portfolio_real.tsv` (format: `TICKER\tName\tUnits\tAvgOpen\tPL\tPLPercent\tNetValue\tStatus`) and `portfolio_tp.tsv` / `portfolio_real_tp.tsv` (format: `TICKER\tTP` or just `TICKER` with no second field if no TP set) to find:
   - **New tickers** (in live scan, not in stored file) → likely a pending order that filled since the last check.
   - **Removed tickers** (in stored file, not in live scan) → position was closed.
   - **TP changed** → user adjusted it manually on eToro since last check (real example caught 2026-09-01: RYTM's real-account TP changed 160.00 → 138.58).
   - Also just report the **pending orders** list from step 5, since those aren't in the stored files at all yet.
8. Write the fresh data back to all 4 files (preserve company names from the old file via a ticker→name lookup dict, since the live page doesn't show a clean company name string easily). Run `python merge_portfolio.py`, then reassemble (`cat part1_fixed.html all_rows.html part3.html > nasdaq-stocks.html`).
9. Report findings to the user in plain language: what's new, what closed, what TP changed, what orders are pending — don't just say "done", the whole point of this feature is surfacing the *changes*.
10. **Auto-chain `SCAN VALUES`**: POST to `http://localhost:8791/scan-portfolio` (start `portfolio_server.py` first if not already running) to refresh analyst Low/Avg/High + dividend yield for all currently-HELD tickers, so anything newly filled/added this pass shows fresh numbers right away. Mention in the report that values were refreshed too, not just structure.

### Known gotcha (2026-09-03): scroll can hang, and a few positions can be permanently invisible in the scroll list

- The `computer{action:"scroll"}` gesture on this specific page can intermittently **time out for 45+ seconds per attempt**, repeatedly, seemingly regardless of pacing between attempts (tried tiny waits, long waits, resizing the window, changing sort order, drag-scroll — none of those fixed it). The only thing that reliably worked was **patience**: keep retrying the exact same small `scroll_amount` (e.g. 2-3) after each hang/timeout: it eventually starts working again mid-session with no code change on our end (looks like a transient eToro-side rendering/websocket load issue, not something to "fix" — just retry). Do not conclude the page is permanently broken after a handful of timeouts.
- **Some individual positions can be invisible in the Manual Trades scroll list at every scroll position**, in both sort directions — a real eToro rendering bug, not a sale. Confirmed 2026-09-03: TCRX, CIFR, FICO, BABA never appeared anywhere while scrolling the full P/L% range (worst-to-best) in the Virtual account, yet all 4 were still genuinely held (verified via `https://www.etoro.com/portfolio/breakdown/{TICKER}`, which always shows the position directly if held, bypassing the virtualized list entirely). **Before concluding a ticker missing from the scroll list was sold, verify it directly via its `/portfolio/breakdown/{TICKER}` page** — much faster than continued scrolling, and it also gives fresh Units/Open/SL/TP/P&L for that one ticker directly.
- Clicking a sort-column header via a raw JS `.click()` (or even a dispatched `MouseEvent` sequence) did **not** change the sort order on this page — it silently no-ops. A real `computer{action:"left_click"}` at the element's actual coordinates (read via `getBoundingClientRect()` if a screenshot isn't available) DID work. General lesson for this SPA: prefer real `computer` actions over synthetic JS dispatch for anything that must actually trigger the app's event handlers, not just bubble a DOM event.
- `computer{action:"screenshot"}` / `zoom` can also time out repeatedly on this page even when plain `javascript_exec` reads keep succeeding — don't assume the whole page is frozen just because image capture fails; verify with a text-based read first.

### Files involved
- `portfolio_virtual.tsv`, `portfolio_real.tsv` — position snapshots (8 tab-separated columns, see step 7).
- `portfolio_tp.tsv`, `portfolio_real_tp.tsv` — TP per ticker.
- `merge_portfolio.py` — injects `data-pf-v-*` / `data-pf-r-*` attributes onto each `<tr>` in `all_rows.html` from these 4 files.

## "SCAN EXIT HISTORY" — realized-profit exit log + re-entry watchlist (added 2026-09-08)

**Trigger phrases**: "SCAN EXIT HISTORY", or a request like "check when I sold X and for how much". Requires a live Claude-in-Chrome session on the user's real eToro login (same constraint as SCAN HOLDINGS/SCAN RED - `https://www.etoro.com/portfolio/history` needs a real authenticated session, can't be scripted headlessly).

**Why this exists**: the user wants to know when a stock they sold for a realized profit (deliberately, to lock in a gain rather than ride it back down) later pulls back to a good re-entry point - the long-term thesis (analyst target) still intact, just cheaper than where they exited. Nothing in this project tracked past exits at all before this - `SCAN HOLDINGS`'s "position was closed" detection only ever reported the closure in the moment, then overwrote the stored file with no permanent record.

**Steps**:
1. Navigate to `https://www.etoro.com/portfolio/history`, filter to **Manual Trades** (the funnel icon), set the date range to the longest available (**1Y**).
2. Switch the account selector (top-left) between **Main Account (Real)** and **Virtual Portfolio** - do this once per account, since exits matter separately per account.
3. `get_page_text` extracts the whole visible table as clean structured text (ticker, invested, units, open price/date/time, close price/date/time, P/L$, P/L%) - no screenshots needed. Click the **"Show More"** button (find it fresh by text each time rather than reusing a stale ref - a stale ref can silently land on a row instead of the button once the DOM re-renders, opening a "Trade Story" popup instead of loading more rows) to load further back, re-extracting with `get_page_text` after a batch of clicks. The Virtual account can have 1000+ rows of test activity; the Real account's is usually far more manageable and more relevant - prioritize Real, extract however much of Virtual seems worthwhile.
4. Save the raw extracted text to a scratch file, then run `python parse_exit_history.py <raw_text_file> <real|virtual>` - parses each closed-position block, keeps ONLY rows that are both actually closed (has a close date) and closed at a **profit** (P/L% > 0, matching the user's stated intent - a stop-loss exit isn't what this log is for), and appends/updates `exit_history.tsv` (TICKER, exit_date, exit_price, pl_pct, account). Re-running for the same ticker+date+account replaces that row, so this is safe to re-run incrementally as more history gets extracted or a new SCAN EXIT HISTORY pass happens later.
5. `check_reentry_opportunities.py` (added to `fundamentals_scan.py`'s own daily LOCAL chain, right after `backtest_signals.py`) reads `exit_history.tsv` alongside the already-scanned `fundamentals_data.tsv` (today's price) and `analyst_targets_*.txt` (average target), and flags a ticker only when BOTH hold: price has dropped at least `PULLBACK_THRESHOLD_PCT` (default 5%) from the exit price, AND the analyst average target still implies at least `UPSIDE_THRESHOLD_PCT` (default 20%) upside from today's price. Writes `REENTRY_WATCHLIST.md`.

**Privacy**: `exit_history.tsv` and `REENTRY_WATCHLIST.md` are both gitignored (same sensitivity as `portfolio_real.tsv` - they reveal real trading activity, which tickers/when/at what profit) - only the two scripts that produce them are committed. This is also exactly why `check_reentry_opportunities.py` only runs in `fundamentals_scan.py`'s LOCAL chain, never in `aggregate_scan_shards.py`'s cloud-parallel chain - the cloud runner's checkout never has (and never should have) `exit_history.tsv` to read.

**Known gotcha**: clicking "Show More" by reusing an earlier `ref_N` (instead of re-finding the button by text each time) can silently stop loading new rows and start opening per-row "Trade Story" popups instead, once the page has re-rendered enough that the old ref now points at a different element. Close the popup (× button, top-right of the modal) and re-find the button fresh if this happens.

### Files involved
- `exit_history.tsv` (gitignored) — the permanent exit log, one row per (ticker, exit_date, account).
- `REENTRY_WATCHLIST.md` (gitignored) — today's re-entry candidates.
- `parse_exit_history.py` — one-time/manual parser, raw eToro history text → `exit_history.tsv`.
- `check_reentry_opportunities.py` — daily automatic checker, `exit_history.tsv` + current data → `REENTRY_WATCHLIST.md`.
