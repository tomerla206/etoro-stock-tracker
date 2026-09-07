# Refresh Log — Green Chunk 10

Chunk file: refresh_green_chunk_10.tsv (341 tickers, all London/AIM + CBOE)

Started: 2026-09-02

## Progress

Processed 1-20 (ANTO through BNZL): all scraped OK, coverage present for all.
Updated (values changed): AZN.L, BARC.L, BHP.L, BLND.L
Unchanged (already matched stored values): ANTO.L, AO.L, ASC.L, ASHM.L, ATG.L, ATYM.L, AUTO.L, AV.L, AVAP.L, AVON.L, BA.L, BAB.L, BAG.L, BATS.L, BBOX.L, BBY.L, BGEO.L, BKG.L (odd but pre-existing wide-spread value, matched, left as-is), BME.L, BMS.L, BMY.L

Processed 21-45 (BOOT through ELM). Updated: BRBY.L, CRDA.L, CTEC.L, DEC.L, DRX.L. Rest unchanged/matched. No lost-coverage cases so far.

Processed 46-70 (EMG through GRG). Updated: ENT.L, EZJ.L, GLEN.L, GPE.L. Rest unchanged/matched. No lost-coverage cases.

Processed 71-100 (GRI through KAP). Updated: HFD.L, HLMA.L, JD.L, JUP.L. Rest unchanged/matched. No lost-coverage cases.

Processed 101-130 (KGF through MONY). Updated: LLOY.L, LMP.L, MICC.L, MKS.L. Rest unchanged/matched. No lost-coverage cases.

Processed 131-160 (MOTR through PAG). Updated: NRR.L, NWG.L, OXB.L, PAF.L. Rest unchanged/matched. No lost-coverage cases.

Processed 161-195 (PAGE through SEIT). Updated: PRU.L, SDLF.L. Rest unchanged/matched. No lost-coverage cases. Noted odd but pre-existing wide-spread values (unchanged, left as-is): PBEE.L, PSN.L.

Processed 196-225 (SEPL through STAN). Updated: SEPL.L, SGE.L, SGRO.L, SHC.L, SRE.L, SSPG.L. LOST COVERAGE: SMSN.L (Samsung Electronics GDR) - widget shows "This stock has no research data". Left row unchanged (was OK/3888.00/3888.00/3888.00), needs manual review.

Processed 226-255 (STJ through TRI). Updated: SUNB.L, SVS.L. Rest unchanged/matched. No new lost-coverage cases.

Processed 256-285 (TRN through VCT). Updated: UTG.L. Rest unchanged/matched. No new lost-coverage cases.

Processed 286-310 (VLX through XPP). Updated: WIZZ.L, WKP.L. Rest unchanged/matched. No new lost-coverage cases.

Processed 311-317 (XPS through ZTF, end of main London list). All unchanged/matched. No new lost-coverage cases. Now moving into London AIM list, starting with 4BB.L (matched, unchanged).

Processed AIM tickers 4BB through DXRX. Updated: ALL.L, CER.L, DXRX.L. Rest unchanged/matched. No new lost-coverage cases.

Processed AIM tickers EAAS through GGP. Updated: FEVR.L, GGP.L. Rest unchanged/matched. No new lost-coverage cases.

Processed AIM tickers GHH through MANO. Updated: HCM.L. Rest unchanged/matched. No new lost-coverage cases.

Processed AIM tickers MIDW through SDI. All unchanged/matched (incl. pre-existing odd wide value SAA.L=19500, left as-is). No new lost-coverage cases.

Processed final AIM tickers SRC through VIC, plus CBOE (Chicago). Updated: THS.L. Rest unchanged/matched. No new lost-coverage cases.

## Final Summary

341/341 tickers processed.

Updated (value changed): AZN.L, BARC.L, BHP.L, BLND.L, BRBY.L, CRDA.L, CTEC.L, DEC.L, DRX.L, ENT.L, EZJ.L, GLEN.L, GPE.L, HFD.L, HLMA.L, JD.L, JUP.L, LLOY.L, LMP.L, MICC.L, MKS.L, NRR.L, NWG.L, OXB.L, PAF.L, PRU.L, SDLF.L, SEPL.L, SGE.L, SGRO.L, SHC.L, SRE.L, SSPG.L, SUNB.L, SVS.L, UTG.L, WIZZ.L, WKP.L, ALL.L, CER.L, DXRX.L, FEVR.L, GGP.L, HCM.L, THS.L
(44 tickers updated with fresh Low/Avg/High)

Flagged lost-coverage (left unchanged, needs manual review): SMSN.L (Samsung Electronics Co Ltd - GDR, London) - widget now shows "This stock has no research data" though row is currently OK/3888.00 flat.

All other ~296 tickers were scraped and found to already match the stored values (no update needed).

No malformed existing rows encountered. No suffix-stripping edge cases (all tickers in this chunk are London/AIM `.L` suffixed, real exchange suffix, queried as-is per method; one Chicago ticker CBOE with no suffix, queried as-is).

