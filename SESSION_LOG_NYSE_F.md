# Session Log — NYSE Letter F

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 61, sourced from `grep '^F' nyse_data.tsv`, sorted. Full list:
F FAF FBIN FBK FBP FBRT FC FCF FCN FCPT FCX FDS FDX FDXF FE FET.US FF FG FHI FHN FICO FIG FIGS FINV FIRY FIS.US FITB FIX FLG FLO FLR.US FLS FMC FMS FMX FN FNB FND FNF FNV FOIL FOR FOUR FPI FPS FR.US FRO FRT FSK FSM FSRNQ FSS FTAI FTI FTRE FTS FTV FUBO FUL FUN.US FVRR

**Progress**: 50/61 done (through FSM). NOT_TRADEABLE: FDXF. NOFAQ: FET.US, FF, FINV, FIRY, FOIL, FOR.

**BLOCKED 2026-08-27 (RESOLVED)**: Hit a CAPTCHA block while loading FSRNQ's eToro `/research` page (Fisker Inc, bankrupt shell). Signature: full-page "Verification Required" / "Slide right to secure your access" challenge, citing "unusual activity" (rapid taps/clicks, automated/bot activity, dev tools). Block ID: `25cf4a4f-df3b-8560-c048-5520aab059d9`. Source IP cited: 46.121.145.37. Stopped immediately per protocol — did NOT attempt to solve/bypass.

**RESUMED 2026-08-27**: Access confirmed clear via AAPL precondition check (real-time price, "Prices by NASDAQ", Trade button enabled, no CAPTCHA/lockout). Redid FSRNQ fresh (tipranks: NOFAQ; eToro: 0.0005, Trade button disabled=true → NOT_TRADEABLE) then completed the remaining 10 tickers: FSS, FTAI, FTI, FTRE, FTS, FTV, FUBO, FUL, FUN.US, FVRR — all OK/TRADEABLE, no further blocks. Letter F now **DONE — 61/61**. Completeness audit passed (both directions, no duplicates) against `nyse_data.tsv`. Final tallies for letter F: 6 NOFAQ (FET.US, FF, FINV, FIRY, FOIL, FOR), 2 NOT_TRADEABLE (FDXF, FSRNQ), 53 OK/TRADEABLE.
