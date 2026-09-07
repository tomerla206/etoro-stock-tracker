# Session Log — Frankfurt Letter D

2026-08-28: Started fresh (strict sequential mode, sole active agent). Login verified via AAPL (314.68, Prices by NASDAQ, Market Closed — normal after-hours, Trade button enabled, account menu present).

Batch 1 (15/29): D6H0.DE, DAM.DE, DAR.DE, DB1.DE, DBAN.DE, DBK.DE, DEF.DE, DEQ.DE, DEX.DE, DEZ.DE, DFTK.DE, DFV.DE, DHER.DE, DHL.DE, DIE.DE — all done, zero blocks.

Notable: DFV.DE's real eToro URL slug is `dfv0.de` (not `dfv.de` — `dfv.de` 404s/redirects to /home). Found via eToro's site search box. Recorded under ticker key `DFV.DE` (matching frankfurt_data.tsv) with data fetched from the `dfv0.de` research page and `DFV0.DE` tipranks widget. DFV.DE came back NOT_TRADEABLE (both Trade buttons disabled) — first NOT_TRADEABLE this letter.

Counts so far: 15 OK/NOFAQ mix — 8 OK, 7 NOFAQ, 1 NOT_TRADEABLE (DFV.DE), 0 CVR.

Resume point: next ticker is DKG.DE (16th of 29).

Batch 2 (29/29, complete): DKG.DE, DLX.DE, DMP.DE, DMRE.DE, DOU.DE, DP4A.DE, DR0.DE, DRW8.DE, DTD2.DE, DTE.DE, DTG.DE, DUE.DE, DWNI.DE, DWS.DE — all done, zero blocks, zero retries beyond normal page-load timing waits.

**LETTER D COMPLETE, 2026-08-28.** Completeness audit: `grep '^D' frankfurt_data.tsv` (29 tickers) vs `analyst_targets_FRANKFURT_D.txt` (29 lines) — diff clean both directions, 0 gaps, 0 extras.

Final tally: 29/29. OK (had analyst coverage): DB1.DE, DBAN.DE, DBK.DE, DEF.DE, DEQ.DE, DEZ.DE, DHER.DE, DHL.DE, DMP.DE, DOU.DE, DTE.DE, DTG.DE, DUE.DE, DWS.DE = 14 OK. NOFAQ (no research data): D6H0.DE, DAM.DE, DAR.DE, DEX.DE, DFTK.DE, DFV.DE, DIE.DE, DKG.DE, DLX.DE, DMRE.DE, DP4A.DE, DR0.DE, DRW8.DE, DTD2.DE, DWNI.DE = 15 NOFAQ (one of these, DFV.DE, is also NOT_TRADEABLE). NOT_TRADEABLE: 1 (DFV.DE). CVR: 0.

Gotcha for future letters: eToro's URL slug does not always match the tsv ticker exactly — DFV.DE's real slug is dfv0.de (found via eToro's own search box after the direct URL redirected to /home). If a `.de` research URL redirects to /home instead of loading the stock page, try the site search box before assuming a block.
