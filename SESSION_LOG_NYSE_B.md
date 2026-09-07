# Session Log — NYSE Letter B

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability).

**Tickers**: 129, sourced from `grep '^B' nyse_data.tsv`, sorted. One CVR-type ticker present: `BPMC CVR` (Sanofi and BPMC Acquisition CVR, price 0.00) — recorded directly from tsv without visiting any site, per protocol.

**Pacing**: randomized 3-6s waits per ticker, ~2-3 tickers per browser_batch call, randomized ~38-40s pause roughly every 2-3 tickers (smaller batches than the nominal 12-15 guidance, but with proportionally more frequent pauses — same per-ticker cadence).

**Progress**: 87/129 tickers completed (B through BOC alphabetically, plus the BPMC CVR row) before the block.

## BLOCK HIT — Cloudflare Error 1015

While fetching ticker **BOH** (Bank of Hawaii Corp), the tipranks widget fetch succeeded normally (low 85.00 / avg 87.20 / high 92.00), but the immediately following eToro `/research` page navigation returned:

```
Error 1015 Ray ID: a30a4da7b880c22f • 2026-08-25 11:37:11 UTC
"You are being rate limited"
"The owner of this website (www.etoro.com) has banned you temporarily from accessing this website."
Cloudflare Ray ID: a30a4da7b880c22f
```

Stopped immediately per mandatory protocol — no retry, no attempt to solve/bypass Cloudflare. BOH's data is incomplete (only the tipranks half was captured) and was deliberately **not** written to `analyst_targets_NYSE_B.txt` — it needs a full fresh fetch (both tipranks and eToro sides) on resume, not a reuse of the partial data above.

**One earlier anomaly noted before the block** (informational, not a block): ticker `BOC` (Boston Omaha Corporation) showed "Delayed prices by NASDAQ" and a gated "Research information is only available to active investors — Sign up" panel on its eToro page, unlike every other ticker in this session which showed real-time/off-hours prices and full access. The Trade button state still read as enabled (not disabled), and the page otherwise loaded normally — this looked like a per-ticker eToro-side restriction (possibly a thinly-traded/legacy listing), not a login or account issue, since the immediately-preceding and following tickers behaved normally. Recorded as NOFAQ/TRADEABLE per the visible data. Worth a sanity re-check on resume if BOC's tradeability is ever in question.

## Resume instructions

- Next ticker to fetch: **BOH** (Bank of Hawaii Corp) — redo both tipranks and eToro sides fresh.
- Before resuming: rigorously re-verify eToro login (AAPL check — real-time price, Trade button enabled, no delayed-price tag) and confirm the Cloudflare ban has lifted (a plain navigation to etoro.com should succeed without the 1015 page). Do not resume immediately — some wait is warranted given this is a rate-limit ban, not a one-off page error.
- Remaining tickers after BOH: BOOT, BORR, BOX, BP.US, BR, BRBR, BRC, BRCC, BRK.B, BRO, BROS, BRSL, BRSP, BRT, BRX, BSAC, BSBR, BSM, BSX.US, BTG.US, BTGO, BTI, BTU, BUD, BUR, BURL, BV.US, BVN, BW, BWA, BWMX, BWXT, BX, BXC, BXDC, BXMT, BXP, BXSL, BY, BYD, BZH (42 tickers left after BOH, so 43 remain total including BOH).

## RESUME 2026-08-26 — block cleared, resumed cleanly

Re-verified login via AAPL check (real-time "309.41 ... Off-hours", "Prices by NASDAQ, in USD" not delayed, Trade button disabled:false). No Cloudflare page. Proceeded with conservative pacing (3-5s per-ticker waits, waits chained in 10s increments for batch pauses since max wait per call is 10s).

**Completed this session so far**: BOH, BOOT, BORR, BOX, BP.US, BR, BRBR, BRC, BRCC, BRK.B (10 tickers) — all clean, no blocks. BOH redone fully fresh (85.00/87.20/92.00, price 76.16, tradeable). BP.US tipranks required bare "BP" (not "BP.US") to resolve — matched correctly (BP plc ADR, 41.00/49.17/58.00). BRCC has an odd analyst-target/price mismatch (target 1.75 vs price 8.55) — recorded as-is per protocol, not fabricated.

File now has 119 lines total (87 prior + 32 new: BOH through BWMX inclusive). All clean, no blocks, 32 straight tickers this session. Next ticker: **BWXT**.
Remaining after BWXT: BX, BXC, BXDC, BXMT, BXP, BXSL, BY, BYD, BZH (8 left after BWXT, 9 total remaining).

## LETTER B COMPLETE — 2026-08-26

All 43 remaining tickers (BOH through BZH) fetched cleanly this session, zero blocks, zero anomalies beyond the two noted above (BP.US tipranks lookup needed bare "BP"; BRCC has an odd target/price mismatch, recorded as-is). Total file: **129/129 lines** (1 CVR row + 128 ticker rows).

**Completeness audit**: diffed `analyst_targets_NYSE_B.txt` against `grep '^B' nyse_data.tsv`, both directions — **0 missing, 0 extra**. Letter B is DONE.

Session totals across both sessions: 129 tickers, 1 CVR (BPMC CVR), several NOFAQ (BAK, BBD, BBDO, BBW, BFS, BH, BHA, BLX, BNT-US, BOC, BTI, BWMX — 12 total), 0 NOT_TRADEABLE found in this letter, rest OK/TRADEABLE.
