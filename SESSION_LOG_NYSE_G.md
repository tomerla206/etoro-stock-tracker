# Session Log — NYSE Letter G

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 78, sourced from `grep '^G' nyse_data.tsv`, sorted. Full list:
G.US GAP GATX GBCI GBTG GBX.US GCO GCTS GD GDDY GDOT GE GEF GEF.B GEL GENI GEO GETY GEV GFF GFI.US GFL GFR GGB GGG GHC GHM GIB GIC GIL GIS GKOS GL GLOB GLP GLW GM GME GME.WS GMED GMRS GNE GNK.US GNL GNRC GNS.US GNW GOLD.US GOLF GOOG.24-7 GOOS GOTU GPC GPI GPK GPMT GPN GPOR GPRK GRBK GRC.US GRCL.CVR GRDN GRND GRNT GROY GS GSBD GSK GSL GTES GTN GTY GVA GWH GWRE GWW GXO

**Progress**: Starting fresh 2026-08-27, after letter F completed cleanly (61/61).

**Note**: GRCL.CVR is a CVR-type ticker (merger contingent-value-rights) — per project convention, record directly as `CVR`/`NOT_TRADEABLE`/`0.00` without visiting the site. GOOG.24-7 and GME.WS may be special (24-7 CFD / warrant) — verify individually.

**Checkpoint 2026-08-27**: 20/78 done (through GFF). No blocks. NOFAQ so far: GBTG, GCTS, GDOT, GEF.B. All others OK/TRADEABLE. Next: GFI.US.

**Checkpoint 2 2026-08-27**: 28/78 done (through GIB). No blocks. Additional NOFAQ: GHC. Next: GIC.

**Checkpoint 3 2026-08-27**: 36/78 done (through GLW). No blocks. Additional NOFAQ: GIC, GLP. Next: GM.

**Checkpoint 4 2026-08-27**: 42/78 done (through GNE). No blocks. NOFAQ: GME. NOT_TRADEABLE: GME.WS (warrant). Next: GNK.US.

**Checkpoint 5 2026-08-27**: 47/78 done (through GNW). No blocks. Additional NOFAQ: GNS.US. Next: GOLD.US.

**LETTER G COMPLETE 2026-08-27**: 78/78 done. Resumed after prior session ran out of shared API quota (not an eToro block, quota since reset) — verified checkpoint was 50/78 (through GOOG.24-7), fetched remaining 28 tickers (GOOS through GXO) with no blocks whatsoever. Additional NOFAQ this stretch: GOTU, GPRK, GRBK, GRC.US, GWH (5 more, total NOFAQ for letter G: GBTG, GCTS, GDOT, GEF.B, GHC, GIC, GLP, GME, GNS.US, GOTU, GPRK, GRBK, GRC.US, GWH = 14). NOT_TRADEABLE: GME.WS (warrant), GRCL.CVR (CVR merger ticker, recorded directly from nyse_data.tsv per convention). GOOG.24-7 recorded as NOT_TRADEABLE (24-7 CFD). All others OK/TRADEABLE. Completeness audit passed: 78/78 both directions, no duplicates. NYSE_LETTER_STATUS.md updated to DONE. Next letter: H (69 tickers, not yet started).
