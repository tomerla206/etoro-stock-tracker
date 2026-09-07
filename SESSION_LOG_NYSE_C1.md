# Session Log — NYSE Letter C1 (C through CNO)

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 82, sourced from `grep '^C' nyse_data.tsv`, sorted, first half (C1). Full list:
C CAAP CABO CACI CAG CAH CAL CALX.US CALY CANG CARR CARS CAT CATO CAVA CB CBAN CBL.US CBRE CBT CBU CBZ CC.US CCEP CCI CCJ CCK CCL CCS CCU CDE CDLR CDP CDRE CE CEPU CF CFG CFR CGAU CHCT CHD CHE CHGG CHH CHPT CHT CHWY CI CIB CIEN CIG CIM CINT CION CL CLB CLF.US CLH CLS CLVT CLW CLX CM CMBT CMC CMCL CMG CMI CMP CMS CMT CMTG CNA CNC CNH.US CNI CNK CNM CNMD CNNE CNO

**Progress**: 82/82 DONE. All clean this session, no blocks (one early transient Chrome extension disconnect, self-resolved, not a site block).

## LETTER C1 COMPLETE — 2026-08-26

Completeness audit: diffed `analyst_targets_NYSE_C1.txt` against the C1 slice (C through CNO) of `nyse_data.tsv` — **0 missing, 0 extra**, 82/82 exact match both directions. Letter C1 is DONE.

No CVR tickers this letter. NOFAQ (11 total): CAL, CATO, CBAN, CCS, CDLR, CEPU, CHGG, CHT, CIG, CION, CMBT. All other 71 tickers OK/TRADEABLE, 0 NOT_TRADEABLE found.
