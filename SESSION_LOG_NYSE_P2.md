# Session Log — NYSE Letter P2

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Split**: Letter P is 87 tickers total, split into P1 (P through PIPR, 43 tickers, DONE) and P2 (PJT through PXED, 44 tickers, this file).

**Tickers (P2)**: 44, sourced from `grep '^P' nyse_data.tsv`, sorted, second half. Full list:
PJT PK PKE PKG PKX PL PLD PLGO PLNT PLOW PLX PM PMT PNC PNFP PNR PNW POR POST PPG PPL PRG PRGO PRI PRIM PRK PRKS PRLB PRM PRMB PRU PS PSA PSFE PSN.US PSO PSQH PSTL PSX PUK PUMP.US PVH PWR PXED

**Progress**: Starting fresh 2026-08-27, immediately after P1 completed (43/43, no blocks in this session). Login already verified fresh via AAPL check earlier in this same session (real-time price 313.38, Market Open, Prices by NASDAQ, Trade button disabled:false x2) — carrying forward, same browser tab/session, no re-verification needed mid-session unless something looks off. Re-verified once more just before starting P2 real work (AAPL 313.86, same signals) — still solid.

**Checkpoint 1 2026-08-27**: 6/44 done (PJT through PL). No blocks. NOFAQ: PKX (1). No NOT_TRADEABLE, no CVR. Next: PLD.

**Checkpoint 2 2026-08-27**: 10/44 done (PJT through PLOW). No blocks. NOFAQ count still 1. No NOT_TRADEABLE, no CVR. Next: PLX.

**Checkpoint 3 2026-08-27**: 15/44 done (PJT through PNFP). No blocks. NOFAQ: PKX, PLX (2). No NOT_TRADEABLE, no CVR. Next: PNR.

**Checkpoint 4 2026-08-27**: 20/44 done (PJT through PPG, halfway). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: PPL.

**Checkpoint 5 2026-08-27**: 24/44 done (PJT through PRI). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: PRIM.

**Checkpoint 6 2026-08-27**: 27/44 done (PJT through PRKS). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: PRLB.

**Checkpoint 7 2026-08-27**: 30/44 done (PJT through PRMB). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Next: PRU.

**Checkpoint 8 2026-08-27**: 33/44 done (PJT through PSA). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. Note: PS (Pershing Square Inc) briefly showed "Market Closed" instead of "Market Open" — not a block signature (price still real-time, Trade button disabled:false x2, normal site chrome) — recorded normally. Next: PSFE.

**Checkpoint 9 2026-08-27**: 37/44 done (PJT through PSQH). No blocks. NOFAQ count still 2. No NOT_TRADEABLE, no CVR. PSN.US special-cased: bare "PSN" tipranks query and eToro's own `/markets/psn.us/research` page both resolve to Parsons Corporation, confirmed matching (same routing-quirk pattern as prior letters' .US tickers) — recorded directly. Next: PSTL.

**Checkpoint 10 2026-08-27**: 40/44 done (PJT through PUK). No blocks. NOFAQ: PKX, PLX, PUK (3). No NOT_TRADEABLE, no CVR. Next: PUMP.US.

**P2 COMPLETE 2026-08-27**: Finished PUMP.US, PVH, PWR, PXED — 44/44 done, no blocks. Completeness audit passed (44/44, both directions, no duplicates). 3 NOFAQ (PKX, PLX, PUK), 0 NOT_TRADEABLE, 0 CVR, 41 OK. PUMP.US special-cased same as PSN.US: bare "PUMP" tipranks query matches eToro's `/markets/pump.us/research` (ProPetro Holding Corp), confirmed via upside-percentage reconciliation. Letter P2 is DONE — full letter P (P1+P2, 87 tickers) now complete.
