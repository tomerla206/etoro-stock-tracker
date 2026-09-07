# Session Log — NYSE Letter R

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers (R)**: 69, sourced from `grep '^R' nyse_data.tsv`, sorted. Full list:
R RACE RAL RAMP RBA RBLX RBRK RC RCI RCL RCUS RDDT RDN RDW.US RDY REA REF REI RELX REPX RES REX REXR REZI RF RGA RGR RH RHI RHP RIG RIO RITM RJF RKT RL RLGT RLI RLJ RLX RM RMAX RMD RNG RNGR RNR RNST ROG ROK ROL RPC.US RPM RPT RRC RRX RS RSG RSI RSKD RTO.US RTX RVLV RVTY RWT RXO RY RYAN RYN RYZ

**Progress**: Starting fresh 2026-08-27, immediately after letters P (P1+P2) and Q completed cleanly in the same session, no blocks. Login verified fresh multiple times earlier in this session — carrying forward, same browser tab/session.

**Checkpoint 1 2026-08-27**: 5/69 done (R through RBA). No blocks. No NOFAQ, no NOT_TRADEABLE, no CVR. Next: RBLX.

**Checkpoint 2 2026-08-27**: 10/69 done (R through RCL). No blocks — one transient "Claude in Chrome is not connected" warning on RCL's javascript_exec call, but the same call's actual result came back with real data (disabled:false x2), and the page text call in the same batch also succeeded normally (Market Open, real-time price) — reads as a momentary extension hiccup, not a login/CAPTCHA/Cloudflare block signature. Verified connection stable with a follow-up check before continuing. No NOFAQ, no NOT_TRADEABLE, no CVR. Next: RCUS.

**Checkpoint 3 2026-08-27**: 14/69 done (R through RDW.US). No blocks. No NOFAQ, no NOT_TRADEABLE, no CVR. RDW.US special-cased: bare "RDW" tipranks query matches eToro's `/markets/rdw.us/research` (Redwire Corp), confirmed via upside-percentage reconciliation. Next: REA.

**Checkpoint 4 2026-08-27**: 18/69 done (R through RELX). No blocks. NOFAQ: RELX (1). No NOT_TRADEABLE, no CVR. Next: REPX.

**Checkpoint 5 2026-08-27**: 21/69 done (R through REX). No blocks. NOFAQ: RELX, REX (2). No NOT_TRADEABLE, no CVR. Next: REXR.

**Checkpoint 6 2026-08-27**: 23/69 done (R through REZI). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: RF.

**Checkpoint 7 2026-08-27**: 26/69 done (R through RGR). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: RH.

**Checkpoint 8 2026-08-27**: 28/69 done (R through RHI). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: RHP.

**Checkpoint 9 2026-08-27**: 30/69 done (R through RIG, nearly halfway). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: RIO.

**Checkpoint 10 2026-08-27**: 32/69 done (R through RITM). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: RJF.

**Checkpoint 11 2026-08-27**: 34/69 done (R through RKT, halfway). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: RL.

**Checkpoint 12 2026-08-27**: 36/69 done (R through RLGT). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: RLI.

**Checkpoint 13 2026-08-27**: 38/69 done (R through RLJ). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: RLX.

**Checkpoint 14 2026-08-27**: 40/69 done (R through RM). No blocks. NOFAQ: RELX, REX, RLX (3). No NOT_TRADEABLE, no CVR. Note: RM briefly showed "Market Closed" like PS earlier in this session — same non-block pattern, recorded normally. Next: RMAX.

**Checkpoint 15 2026-08-27**: 42/69 done (R through RMD). No blocks. NOFAQ: RELX, REX, RLX, RMAX (4). No NOT_TRADEABLE, no CVR. Next: RNG.

**Checkpoint 16 2026-08-27**: 44/69 done (R through RNGR). No blocks. NOFAQ count still 4. No NOT_TRADEABLE, no CVR. Next: RNR.

**Checkpoint 17 2026-08-27**: 46/69 done (R through RNST). No blocks. NOFAQ count still 4. No NOT_TRADEABLE, no CVR. Next: ROG.

**Checkpoint 18 2026-08-27**: 48/69 done (R through ROK). No blocks. NOFAQ count still 4. No NOT_TRADEABLE, no CVR. Next: ROL.

**Checkpoint 19 2026-08-27**: 51/69 done (R through RPM). No blocks. NOFAQ: RELX, REX, RLX, RMAX, RPC.US (5). No NOT_TRADEABLE, no CVR. IMPORTANT correction: initially assumed RPC.US matched bare-ticker "RPC" (RPC Inc, oilfield services, tipranks Low/Avg/High 11.00/13.00/15.00) per the routing-quirk pattern used successfully for PSN.US/PUMP.US/QUAD.US — but eToro's own `/markets/rpc.us/research` page shows RPC.US is actually "Ridgepost Capital Inc", a completely different company, confirmed by `nyse_data.tsv` (blank consensus/rating for RPC.US). Caught before recording — discarded the bare-RPC data and correctly recorded RPC.US as NOFAQ (name Ridgepost Capital Inc, price 8.80). Lesson: the bare-ticker fallback is not universally safe — always verify eToro's displayed company name and/or tsv baseline before trusting it, not just upside-percentage math. Next: RPT.

**Checkpoint 20 2026-08-27**: 53/69 done (R through RRC). No blocks. NOFAQ count still 5. No NOT_TRADEABLE, no CVR. RPT double-checked against tsv (Rithm Property Trust Inc, confirmed match). Next: RRX.

**Checkpoint 21 2026-08-27**: 55/69 done (R through RS). No blocks. NOFAQ count still 5. No NOT_TRADEABLE, no CVR. Next: RSG.

**Checkpoint 22 2026-08-27**: 57/69 done (R through RSI). No blocks. NOFAQ count still 5. No NOT_TRADEABLE, no CVR. Next: RSKD.

**Checkpoint 23 2026-08-27**: 59/69 done (R through RTO.US). No blocks. NOFAQ: RELX, REX, RLX, RMAX, RPC.US, RTO.US (6). No NOT_TRADEABLE, no CVR. RSKD's first Trade-button check came back an empty array (page still loading) — re-checked 3s later, came back clean (disabled:false x2, real-time price, Market Open) — not a block, just a load-timing hiccup. RTO.US applied the RPC.US lesson: cross-checked tsv first (blank consensus confirmed), recorded as NOFAQ directly without trying the bare-ticker fallback. Next: RTX.

**Checkpoint 24 2026-08-27**: 61/69 done (R through RVLV). No blocks. NOFAQ count still 6. No NOT_TRADEABLE, no CVR. Next: RVTY.

**Checkpoint 25 2026-08-27**: 63/69 done (R through RWT). No blocks. NOFAQ count still 6. No NOT_TRADEABLE, no CVR. Next: RXO.

**Checkpoint 26 2026-08-27**: 65/69 done (R through RY). No blocks. NOFAQ count still 6. No NOT_TRADEABLE, no CVR. Next: RYAN.

**R COMPLETE 2026-08-27**: Finished RYAN, RYN, RYZ — 68/69 tickers done at that point, no blocks. Ran completeness audit against the expected list and against `nyse_data.tsv` directly — caught that **RDY was skipped during execution** (present in the original planned ticker list between RDW.US and REA, but never actually fetched). Fetched RDY fresh (Dr. Reddys Laboratories Limited, Low/Avg/High 16.14/16.14/16.14, price 12.17, TRADEABLE) and appended. Re-ran the audit: 69/69, both directions, no duplicates — passed. Final counts: 7 NOFAQ (RELX, REX, RLX, RMAX, RPC.US, RTO.US, RYZ), 0 NOT_TRADEABLE, 0 CVR, 62 OK. Letter R is DONE. Lesson: always run the tsv-direct completeness check, not just against the session's own remembered ticker list — the remembered list itself can silently skip an entry during long manual sequences.
