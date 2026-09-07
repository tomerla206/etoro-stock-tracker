# Session Log — NYSE Letter N

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 74, sourced from `grep '^N' nyse_data.tsv`, sorted. Full list:
NABL NAK NAT NATL NBHC NBR NCLH NE NEE NEM NET NEU NEXA NFG NG.US NGG NGS NGVC NGVT NHC NHI NI NIC NIO NIQ NJR NKE NLOP NLY NMAX NMR.US NNI NNN NOAH NOC NOG NOK NOMD NOTE NOV NOW NP NPK NPKI NPO NPWR NRDY NRG NRGV NSC NSP NSTB NTB NTR NTST NU NUE NUS NUVB NVDA.24-7 NVGS NVO NVR NVS NVST NVT NWG NWN NX NXDR NXDT NXE NXRT NYT

**Progress**: Starting fresh 2026-08-27, immediately after letter M (M1+M2, 100 tickers) completed cleanly, no blocks. Login already verified via AAPL check at session start (still valid, same browser session).

**Checkpoint 1 2026-08-27**: 22/74 done (NABL through NI). No blocks. NOFAQ so far: NEU, NGG, NHC (3). No NOT_TRADEABLE, no CVR yet. Note: NG.US initially looked like it might be NOFAQ (tipranks query with literal "NG.US" returns no data), but cross-checked with bare ticker "NG" on tipranks and got real matching analyst data (upside % matches eToro price almost exactly) — recorded as OK using the bare-ticker data, similar judgment call to prior letters' routing quirks. Next: NIC.

**Checkpoint 2 2026-08-27**: 30/74 done (NABL through NMAX). No blocks. NOFAQ so far: NEU, NGG, NHC, NLOP (4). No NOT_TRADEABLE, no CVR yet. Next: NMR.US.

**Checkpoint 3 2026-08-27**: 37/74 done (NABL through NOK, halfway). No blocks. NOFAQ so far: NEU, NGG, NHC, NLOP (4). No NOT_TRADEABLE, no CVR yet. NMR.US special-cased same as NG.US: literal ".US" ticker query on tipranks returns no data, but bare ticker ("NMR") has real matching analyst data — recorded as OK. Next: NOMD.

**Checkpoint 4 2026-08-27**: 45/74 done (NABL through NPO). No blocks. NOFAQ so far: NEU, NGG, NHC, NLOP, NOTE (bankrupt-shell-priced, $0.0617, but still TRADEABLE), NPK (6 total). No NOT_TRADEABLE, no CVR yet. Next: NPWR.

**Checkpoint 5 2026-08-27**: 51/74 done (NABL through NSP). No blocks. NOFAQ count still 6, no NOT_TRADEABLE, no CVR. Next: NSTB.

**Checkpoint 6 2026-08-27**: 58/74 done (NABL through NUS). No blocks. NOFAQ: NEU, NGG, NHC, NLOP, NOTE, NPK, NUS (7). NOT_TRADEABLE: NSTB (bankrupt-shell SPAC, price $0.0099). No CVR yet. Next: NUVB.

**Checkpoint 7 2026-08-27**: 63/74 done (NABL through NVR). No blocks. NVDA.24-7 confirmed NOFAQ+NOT_TRADEABLE per established .24-7 CFD pattern. NOFAQ total 8, NOT_TRADEABLE total 2 (NSTB, NVDA.24-7). No CVR yet. Next: NVS.

**Checkpoint 8 2026-08-27**: 68/74 done (NABL through NWN). No blocks. Only 6 tickers remain: NX, NXDR, NXDT, NXE, NXRT, NYT. No CVR encountered in this letter at all. Next: NX.

**LETTER N COMPLETE 2026-08-27**: 74/74 done. No blocks whatsoever this entire letter. Final NOFAQ list: NEU, NGG, NHC, NLOP, NOTE (bankrupt-shell-priced, $0.0617, still TRADEABLE), NPK, NUS, NXDT, plus NVDA.24-7 and NSTB which are also NOT_TRADEABLE — 10 NOFAQ total. NOT_TRADEABLE: NSTB (bankrupt-shell SPAC, price $0.0099), NVDA.24-7 (CFD variant, per established pattern) — 2 total. No CVR tickers in this letter. Two ".US" tickers (NG.US, NMR.US) special-cased: tipranks literal-ticker query returns no data, but the bare ticker (NG / NMR) has real matching analyst data (upside % matches eToro price) — both recorded as OK using the bare-ticker data, consistent with prior letters' routing-quirk judgment calls (IR/TT in letter I, MKC/V in letter M1). Completeness audit passed: 74/74 both directions, no duplicates. NYSE_LETTER_STATUS.md updated to DONE. Next letter: O (49 tickers, not yet started).
