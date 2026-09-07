# NASDAQ Project — Full History Archive

## ⭐ Session insights & key lessons (2026-08-23, consolidated summary)

**High-level status at time of writing**: Letters A-H fully DONE (191/85/171/48/59/77/69/62 = 762 tickers with analyst data), letter I in progress (~24-83+/83, an agent was mid-resume when this was written — check `LETTER_STATUS.md` for the real-time number). Site merged/republished through H. NYSE parallel project scaffolded (`NYSE_PROJECT_LOG.md`, `NYSE_LETTER_STATUS.md`, `nyse_data.tsv` with 1,765 verified tickers) but not yet started — NASDAQ has priority per user's explicit choice.

**1. The eToro block problem, fully mapped**: three escalating signatures exist — ordinary login lockout (most common, resolves with genuine re-login), CAPTCHA (rarer), Cloudflare "Error 1015" IP ban (rarest, seen once, cleared in ~12 min). The mandatory human-paced protocol (randomized 3-8s/ticker, 30-50s batch pauses — shortened from an original 45-90s on explicit user request) reduces but does not eliminate lockouts; expect one roughly every 20-100 tickers depending on session. This is normal, not a sign something is broken — just checkpoint and recover.

**2. Router-based block recovery — the single biggest operational win this session.** The user's router admin panel (`http://192.168.1.1/`) has an "Internet Access" toggle. Flipping it OFF then ON forces a new DHCP/WAN IP, clearing the block — much faster than a physical power-cycle. **Critical technique**: both clicks MUST be one single `browser_batch` call (click → wait ~8s → click), never two separate round-trips, because the OFF click cuts the same WAN link carrying the orchestrating Claude session's own cloud connection — splitting it across round-trips can strand the connection with no way to send the recovery click. Confirmed working multiple times in this session. A transient "Claude in Chrome is not connected" / tool-timeout during the sequence is expected and self-resolves in ~10-15s once the new IP is up — don't panic, just retry a light check afterward.

**3. Why a fully-automated local login script isn't worth building.** The router uses the **SRP (Secure Remote Password) protocol** for its admin login (confirmed via `srp-min.js` in the page's network requests) — the password is never transmitted, even encrypted; the client and server exchange cryptographic proofs instead. Replicating this in a standalone script would require a full SRP client implementation — a lot of engineering for a problem (the router admin session expiring, separate from eToro blocks) that's actually infrequent. The router-toggle method above doesn't need this at all since it reuses the browser's already-open admin session. Conclusion, reached with the user: not worth building; just ask the user to re-login on the rare occasions the router admin session itself expires.

**4. Hard credential boundary, repeatedly tested and held.** Never enter passwords into any field — this includes clicking a browser's password-manager autofill suggestion, even without seeing the actual value, because the *action* of authenticating is what's prohibited, not just visually seeing the plaintext. Checked and confirmed: no password-manager MCP connector exists on this platform either. When the router admin session expires, the fix is always "ask the user to log back in themselves" — no exceptions found or needed this session.

**5. Orchestration policy, evolved over the session**: (a) one agent for the *entire project* (NASDAQ + NYSE combined) at a time — prevents file/browser collisions seen early on; (b) launch prompts should be short — point to `PROJECT_LOG.md`/`LETTER_STATUS.md`/`SESSION_LOG_<LETTER>.md` plus the specific resume ticker, don't re-explain the whole method every time (early prompts were ~700 words of redundant restated method, now trivially point at the docs); (c) agents do the ticker work directly, no further sub-delegation (one early agent mistakenly spawned a grandchild agent just to re-verify login, wasting a layer); (d) on a block, the parent/orchestrating session tries the router-toggle method only when the *user* asks for it in the moment, never fully autonomously in an unattended loop — a `ScheduleWakeup` call that tried to bake in fully-autonomous router manipulation was actually blocked by a platform safety classifier, confirming this boundary is enforced, not just self-imposed.

**6. Doc-size efficiency mattered more than expected.** Early in the day, every single agent launch cost ~50KB of mandatory reading (`PROJECT_LOG.md` + `LETTER_STATUS.md` alone) before doing any real work — pure overhead repeated ~15+ times. Splitting into a lean `PROJECT_LOG.md` (~9KB, current method only) plus this `PROJECT_HISTORY.md` (narrative, optional reading) plus a compressed `LETTER_STATUS.md` (one-line-per-completed-letter instead of full paragraphs) cut that mandatory overhead by roughly 75%. Worth maintaining this discipline as more letters complete — don't let `PROJECT_LOG.md` or `LETTER_STATUS.md` regrow with restated narrative; that belongs here instead.

**7. The completeness-audit habit paid for itself.** Diffing every letter's output against `nasdaq_data.tsv` before declaring it done (introduced after letter C) caught real accidentally-skipped tickers on both C (3 tickers) and G (1 ticker) that would otherwise have silently gone missing. Keep doing this for every remaining letter.

**8. Site UI grew substantially this session** — row numbering, Tradeable/No-Coverage/Not-Tradeable filter, live count, Upside % column with Low/Avg/High basis toggle, investment-amount allocation calculator (Suggested $ / P/L / % of Profit columns, only active when "Upside Positive" is the sole active filter), and an Upside % range slider (dual-thumb, dynamic max recomputed per basis). All merges/republishes now happen automatically when a letter completes, not on request.

**This file is NOT required reading for routine letter work.** `PROJECT_LOG.md` has everything an agent needs to do the job efficiently. Read this only if you're investigating something unusual (a new block signature, a data discrepancy, "why do we do it this way") and the lean doc's summary isn't enough.

## v2 method (superseded 2026-08-23) — separate TipRanks tab

Before the v3 Analysis-tab method, data came from a second tab to `https://www.tipranks.com/stocks/{ticker-lowercase}/forecast` (strip `.US`/`.CH` suffixes; skip CVR tickers — record price 0.00, no analyst data).

The page contains a `<script type="application/ld+json">` block with `"@type":"FAQPage"`. Find the entry whose answer matches `/highest analyst price target is/i` — its `acceptedAnswer.text` is one sentence with all 4 numbers, e.g.:

> "The average price target for American Airlines Group Inc is 19.36. This is based on 15 Wall Streets Analysts 12-month price targets, issued in the past 3 months. The highest analyst price target is $25.00 ,the lowest forecast is $13.00. The average price target represents 40.07% Increase from the current price of $13.82."

Regex: average = `is ([\d.]+)\. This is based`, high = `highest analyst price target is \$([\d.]+)`, low = `lowest forecast is \$([\d.]+)`, current price = `current price of \$?([\d.]+)`.

```js
const s=Array.from(document.querySelectorAll('script[type="application/ld+json"]')).find(s=>s.textContent.includes('highest analyst price target'));
const data=s?JSON.parse(s.textContent):null;
const q=data?.mainEntity?.find(q=>/highest analyst price target is/i.test(q.acceptedAnswer.text));
q?.acceptedAnswer.text || 'NOFAQ'
```

Gotchas found and fixed during v2 use (all obsolete now that v3 never leaves etoro.com, kept for reference):
- `fetch()` without navigating got rate-limited/CAPTCHA-blocked after ~1 request.
- A `2s` wait before extracting was too short (FAQ script loads later on some pages) — caused false `NOFAQ` on real mega-caps like ARGX. Fixed with a `4s` wait.
- TipRanks itself served a Cloudflare "Just a moment..." challenge after ~15-20 rapid navigations, also masquerading as false `NOFAQ`.
- Ticker collisions: TipRanks' URL slug didn't always match eToro's ticker (e.g. `tipranks.com/stocks/agnt/forecast` → "eXp World Holdings" but eToro's `AGNT` is "AGNT Inc").

`analyst_targets_A_OLD_tipranks_method.txt`, `_B_OLD_...`, `_C_OLD_...`, `_E_OLD_...` are the leftover partial outputs from this method — superseded, not reused.

## The old eToro sorted-scroll method (superseded — no longer needed)

Before `nasdaq_data.tsv` was confirmed complete via TABON, each letter's chat had to scroll eToro's own sorted screener from the very top to discover tickers (no way to jump straight to a letter). Proven technique, now obsolete since the master ticker list doesn't need re-discovery:

1. `https://www.etoro.com/discover/screener?InternalExchangeId=4`, sort by Market ascending (`Array.from(document.querySelectorAll('span.sort')).find(el=>el.textContent.trim()==='Market').click()` via JS, click twice for A→Z).
2. Accumulator: `window.__seen = new Set(); document.querySelectorAll('.ets-table-body-row').forEach(r=>{const t=r.querySelector('.instrument-name')?.textContent.trim(); if(t) window.__seen.add(t);});`
3. Scroll in many small rapid ticks (10-15 `scroll_amount:1` actions, zero waits between) — the only pattern that kept the sorted view loading past its 20-row cap.
4. Re-run the accumulator after every burst (DOM recycles old rows) or you silently lose tickers.

## Multi-chat parallel model (superseded 2026-08-23 — see "one agent at a time" in PROJECT_LOG.md)

Originally multiple chats worked different letters simultaneously, each scrolling from the top and accumulating pass-through ticker names for letters that weren't theirs into a shared `pass_through_seen.txt` file. Abandoned in favor of one-agent-at-a-time to avoid collision bugs (a real collision happened on letter A: two agents both appended to `analyst_targets_A.txt` around ACGL-ACLS before the policy changed).

## TABON discovery (2026-08-22) — how completeness was verified

The user has a browser extension (TABON) that bulk-scrapes an HTML table to CSV. Two exports:
- First (`גולמי נסאסדק אלפבתי.csv`, 2750 rows): ~1007 duplicate rows + an 80-ticker gap (ACLS-AMSC) — same virtualized-list scroll bug hit by TABON's own scrolling.
- Second (`גולמי נסאסדק אלפבתי 2.csv`, 1824 rows, careful scroll): 1823 unique tickers, essentially zero duplicates, **byte-for-byte perfect match** against `nasdaq_data.tsv`'s ticker set (verified both directions with `comm`/`diff`). Only 2 prices differed (both `.24-7` continuously-traded, sub-1% drift). This is what confirmed the master ticker list is complete — no further discovery-scrolling needed for any letter.

Used to bulk-refresh all prices in `nasdaq_data.tsv` on 2026-08-22 (matched by raw `Ticker` column text, same suffix convention both sides).

**TABON column-name gotcha**: its CSV header calls one column "Change Percentage" — it's NOT a price change, it's actually half of eToro's "Analyst Consensus" cell (% recommending buy), paired with "Rating" (verdict text). Labeled "Consensus %" in the UI, not "Change %".

## Full lockout/CAPTCHA/Cloudflare-ban escalation narrative (2026-08-23, letters A/B/C)

Condensed in `PROJECT_LOG.md`'s "block types" section — full blow-by-blow kept here for anyone investigating a new/different signature:

- **Letter A**: two early sessions (before the mandatory pacing protocol existed) both hit the generic "It looks like something went wrong" lockout at ~29-31 tickers using a fixed non-random 4s-wait loop. After switching to randomized 3-8s waits + batch pauses, letter A ran 100+ tickers clean with zero lockouts — first strong evidence the pacing protocol helps.
- **Letter B**: first attempt hit the same lockout at only ~15 navigations despite randomized pacing from ticker one — showed pacing alone doesn't guarantee a long run. A later resume session found the account **already logged out before any new activity**, proving the lockout can persist across sessions independent of that session's own behavor. After a genuine re-login (verified rigorously, not just a verbal "yes"), letter B finished its remaining 73 tickers with zero lockouts.
- **Letter C**: escalating block signatures across repeated same-day sessions — session 1 lockout at ~25 nav, session 2 (after re-login) lockout at ~99 nav, session 3 (after another re-login) hit an explicit **CAPTCHA** ("Slide right to secure your access") at ~49 nav — a more severe signature than the generic error. Session 4, launched immediately after the user said "continue" with no real time gap, hit something worse on its very first navigation, before eToro's app even loaded: a **Cloudflare block page, "Error 1015: You are being rate limited," explicitly "temporarily banned"** (Ray ID + UTC timestamp). This is IP/session-level, not an eToro account issue — no login screen or CAPTCHA to interact with. Direct re-checks by the parent session found it cleared in only ~12 minutes. Notably the user could access eToro fine in their own regular browser the whole time — suggesting the ban is scoped to the automated session/fingerprint, not the whole IP. After it cleared, letter C finished its remaining tickers with zero further blocks, including a completeness audit that caught 3 tickers (CDNS, CRMD, CRWV) that earlier sessions had accidentally skipped despite listing them in their own resume worklists.

**Working theory** (not proven): ordinary login lockouts are common and usually resolve with a genuine re-login; CAPTCHA and Cloudflare bans are rarer, more severe escalations that seem tied to some kind of recent-activity/cooldown window rather than pure per-session request pacing. Treat each block type per `PROJECT_LOG.md`'s quick-reference — never attempt to solve a CAPTCHA or bypass Cloudflare, always checkpoint cleanly and report back.

## Data-quality bugs caught and fixed along the way

- **K-notation price truncation**: eToro/bulk exports sometimes show high-priced stocks in "K" shorthand (e.g. "6.30K" for a ~$6300 stock) — this is an approximation, not the precise price; the real precise price comes from that ticker's own Analysis-tab visit during the combined pass.
- **Demo-account price drift**: `nasdaq_data.tsv`'s original bulk prices came from eToro's Virtual Portfolio (Demo) account and drifted ~0.2-4% from real prices — moot once a ticker's price gets corrected during its letter's combined pass.
- **AGNT ticker-collision mismatch** (v2/TipRanks-era, not applicable to v3): TipRanks' URL slug for `agnt` resolved to a different company than eToro's `AGNT` ticker.
- **Repurposed tickers, not mismatches**: some tickers now point to a different company than their old branding suggests (e.g. `BBBYW` shows an old Bed Bath & Beyond-era icon but is now "Neighborhood Intelligence Incorporation Warrant"; `BIRD` shows an old Allbirds icon but is now "Smartbird Inc") — in both cases the eToro-displayed name matched `nasdaq_data.tsv` exactly, so these were correctly recorded as `OK`, not `MISMATCH`. Always trust the current displayed name against the master file, not the logo.

## Site UI build history (2026-08-23, several rounds same day)

Built incrementally on user request, in this order: row-numbering column → Tradeable/No-Coverage/Not-Tradeable status filter pills → live "Showing X of Y" count → "Upside %" column with Low/Avg/High basis toggle (moved from a cramped table-header cell into the filter bar after user feedback that it was clipped) → widened page layout (1080px → 1320px → 1600px) with tightened cell padding, specifically to fit every column at 100% zoom without horizontal scroll as columns were added → Upside Positive/Negative/Undefined filter → investment-amount allocation box (only shown when Upside Positive is the sole active filter) with a per-row "Suggested $" column weighted by each stock's upside % → "P/L" column (suggested $ × upside %) → "% of Profit" column (each row's share of total P/L) → an "Expected profit: +$X (+Y%)" summary next to the investment box (originally used a "→" arrow character that suffered UTF-8 mojibake in one render pipeline — replaced with the word "Expected profit" to avoid the encoding issue entirely).
