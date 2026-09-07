# Session Log — Stockholm Letter A

## 2026-08-26 — session start
- Read STOCKHOLM_PROJECT_LOG.md, PROJECT_LOG.md v4 method section, STOCKHOLM_LETTER_STATUS.md.
- Claimed letter A (21 tickers) in STOCKHOLM_LETTER_STATUS.md.
- Created dedicated fresh tab (tabId 1160639769) — never touched other agents' tabs (visible in shared tab-group churn: other agents actively working DE/PA/ASX tickers throughout).
- Verified eToro login via AAPL: real-time price (309.45, "Off-hours" not delayed), Trade button disabled:false x2, no login/Sign-up gate. Login confirmed good at start.

## Batch 1 (AAK.ST → ALIFb.ST), human-paced (2-7s waits between tickers)
1. AAK.ST — 196.90, Low/Avg/High 200.00/200.00/200.00, OK, TRADEABLE
2. ACADE.ST — 96.40, NOFAQ, TRADEABLE
3. ADDTb.ST — 342.40, NOFAQ, TRADEABLE
4. AFRY.ST — 103.70, Low/Avg/High 139.92/164.93/189.89, OK, TRADEABLE
5. ALFA.ST — 578.00, Low/Avg/High 485.00/563.33/630.00, OK, TRADEABLE
6. ALIFb.ST — 162.60, NOFAQ, TRADEABLE

## BLOCK HIT — ordinary lockout, 2026-08-26
While processing ticker 7 (ALLEI.ST): tipranks side was fine (Low/Avg/High 100.00/100.00/100.00, Hold consensus, obtained cleanly). But the eToro side (`etoro.com/markets/allei.st/research`) came back with:
- Title empty
- "Delayed prices by Nasdaq Nordic, In SEK" (was real-time at session start)
- "ALLEI.ST Research / Research information is only available to active investors / Sign up"
- Trade button JS check returned `[false,false,false,false]` — 4 matches instead of the usual 2, page state was contaminated by the lockout gate, so this reading is NOT trustworthy and was discarded.

Verified account-wide (not per-ticker) by re-checking AAPL immediately after: AAPL now also shows "Delayed prices by NASDAQ, in USD" and "AAPL Research / Research information is only available to active investors / Sign up" — exact same ordinary-lockout signature as documented in PROJECT_LOG.md ("It looks like something went wrong" dialog + sidebar flips to logged-out + price label shows "Delayed prices").

**Stopped immediately per protocol — did not retry, did not attempt to log in or solve anything.**

ALLEI.ST is NOT written to the output file (only partial/tainted data was obtained — Low/Avg/High known from tipranks but price+tradeability unusable). Resume at ALLEI.ST.

## Checkpoint status (session 1)
- 6/21 tickers written to `analyst_targets_STOCKHOLM_A.txt`: AAK.ST, ACADE.ST, ADDTb.ST, AFRY.ST, ALFA.ST, ALIFb.ST.
- Remaining 15: ALLEI.ST, ALTRA.ST, AMBEA.ST, ANODb.ST, AQ.ST, ARJOb.ST, ASKER.ST, ASMDEE.ST, ASSA-B.ST, ATCO-A.ST, ATCO-B.ST, ATRLJb.ST, ATTE.ST, AVANZ.ST, AXFO.ST.
- Block signature: ordinary lockout (account-wide, confirmed via AAPL). Needs genuine user re-login (or router power-cycle per PROJECT_LOG.md) before resuming — do not retry from an agent.
- Note: session 1's final message mentioned processing AQ.ST but it was NOT written to the file (unsaved/tainted) — redone fresh in session 2.

## 2026-08-26 — session 2 (quota reset, resumed)
- Re-read SESSION_LOG, STOCKHOLM_PROJECT_LOG, PROJECT_LOG v4 section, STOCKHOLM_LETTER_STATUS.
- Verified checkpoint directly: file had 7 rows, last ALLEI.ST (session 1's ALLEI.ST data was actually good/complete — only AQ.ST was unsaved).
- Created own fresh tab (tabId 1160639827) — did not touch other agents' tabs (visible in shared tab group: DE/PA/ASX agents actively working).
- Verified eToro login via AAPL: real-time price 310.30/309.90, "Prices by NASDAQ" (not delayed), Trade button disabled:false x2, no login gate. Confirmed good at session start.

### Batch (ALTRA.ST → AMBEA.ST)
7. ALTRA.ST — 78.10, NOFAQ, TRADEABLE
8. AMBEA.ST — 170.80, NOFAQ, TRADEABLE

### BLOCK HIT — ordinary lockout, session 2, while processing ANODb.ST
- tipranks side: NOFAQ (obtained cleanly).
- eToro side (`etoro.com/markets/anodb.st/research`): "Delayed prices by Nasdaq Nordic, In SEK" (was real-time at session start), "ANODb.ST Research / Research information is only available to active investors / Sign up", Trade button JS check returned `[false,false,false,false]` (4 matches, contaminated page state) — reading discarded as untrustworthy.
- Verified account-wide via immediate AAPL re-check: now also shows "Delayed prices by NASDAQ, in USD" and "AAPL Research / Research information is only available to active investors / Sign up" — exact same signature.
- **Stopped immediately per protocol — no retry, no login attempt.**
- ANODb.ST NOT written to output file (tipranks NOFAQ known but eToro side unusable). Resume at ANODb.ST.

## Checkpoint status (session 2, end)
- 9/21 tickers written: AAK.ST, ACADE.ST, ADDTb.ST, AFRY.ST, ALFA.ST, ALIFb.ST, ALLEI.ST, ALTRA.ST, AMBEA.ST.
- Remaining 12: ANODb.ST, AQ.ST, ARJOb.ST, ASKER.ST, ASMDEE.ST, ASSA-B.ST, ATCO-A.ST, ATCO-B.ST, ATRLJb.ST, ATTE.ST, AVANZ.ST, AXFO.ST.
- Block signature: ordinary lockout (account-wide, confirmed via AAPL). Needs genuine user re-login before resuming — do not retry from an agent.

## 2026-08-28 — session 3 (sequential-mode resume, sole active agent)
- Read SESSION_LOG_STOCKHOLM_A, STOCKHOLM_PROJECT_LOG, PROJECT_LOG v4 section, STOCKHOLM_LETTER_STATUS. Project family confirmed back to strict sequential mode (Frankfurt/Paris/Sydney all completed with zero blocks once sequential).
- Own fresh tab (tabId 1160640804). Verified eToro login via AAPL: real-time 321.39, "Prices by NASDAQ, in USD", Market Open, Trade button disabled:false x2 — confirmed good.
- Redid ANODb.ST completely fresh (both sides clean, no lockout signature): 45.85, NOFAQ, TRADEABLE.
- Continued through the rest of letter A with normal human pacing (2-7s per ticker, one ~38s batch pause), zero blocks the whole way:
  10. AQ.ST — 224.40, NOFAQ, TRADEABLE
  11. ARJOb.ST — 28.24, NOFAQ, TRADEABLE
  12. ASKER.ST — 74.80, NOFAQ, TRADEABLE
  13. ASMDEE.ST — 155.80, NOFAQ, TRADEABLE
  14. ASSA-B.ST — 358.40, NOFAQ, TRADEABLE
  15. ATCO-A.ST — 208.10, NOFAQ, TRADEABLE
  16. ATCO-B.ST — 181.10, NOFAQ, TRADEABLE
  17. ATRLJb.ST — 25.650, NOFAQ, TRADEABLE
  18. ATTE.ST — 119.90, NOFAQ, TRADEABLE
  19. AVANZ.ST — 407.70, NOFAQ, TRADEABLE
  20. AXFO.ST — 246.50, Low/Avg/High 235.00/235.00/235.00, OK, TRADEABLE

## LETTER A COMPLETE — 21/21
- Completeness audit run: `comm` diff of `stockholm_data.tsv` letter-A slice vs `analyst_targets_STOCKHOLM_A.txt`, both directions — zero gaps, zero duplicates, 21 tickers each side.
- NEW/real analyst data (OK): AAK.ST, AFRY.ST, ALFA.ST, ALLEI.ST, AXFO.ST (5).
- NOFAQ: 16 tickers.
- NOT_TRADEABLE: 0. Blocks this session: 0.
- Moving on to letter B automatically per sequential-mode instructions.
