# Refresh Log — Green Chunk 2

Chunk file: refresh_green_chunk_02.tsv (394 tickers, all NASDAQ)
Method: REFRESH_METHOD.md (TipRanks widget, per-ticker, 15-20s paced)
Completed 2026-09-02.

## Summary

394/394 tickers processed. All 394 successfully updated with fresh Low/Avg/High values
in their respective analyst_targets_*.txt files. 0 tickers flagged as lost-coverage
(every ticker in the chunk still had an ANALYST PRICE TARGET section on the widget).
0 malformed existing rows encountered.

## Suffix stripping applied (per REFRESH_METHOD.md rules)

- PCT.US -> queried as PCT
- SSYS.US -> queried as SSYS
- CCC.US -> queried as CCC
- GTX.US -> queried as GTX
- OM.US -> queried as OM
- KELYA.US -> queried as KELYA
- IQ.US -> queried as IQ
- SSP.US -> queried as SSP
- NWPX.US -> queried as NWPX
- LMNR.US -> queried as LMNR
- AUDC.US -> queried as AUDC

All other tickers in the chunk had no suffix and were queried as-is.

## Anomalies / notes

- A few tickers returned Low=Avg=High identical values (single-analyst or all-analysts-agree
  cases) — this is expected per the method, not an error: SMPL, RDNT, HUBG, ERII, GGAL, PSMT,
  SCHL, PSNY, TCMD, IOSP, DORM, MBUU, JJSF, RUM, WABC, CTBI, PLAB, CVCO, HSAI, ITRN, CHCO,
  AFYA, DSGR, IMXI, LOCO, ANIK, CASS, UFCS, TILE, GSBC, GPGI, WINA, FNKO, CGBD, CRAI, TFSL,
  HCM (no — HCM had a range), REYN, AIRS, KE, MCFT, and several bank/small-cap tickers.
- One transient browser-extension disconnect occurred mid-session (during BMEA lookup);
  recovered immediately on retry with no data loss.
- A couple of tickers (CCOI, MERC, BBSI, SENEA, DH, ASTS, JANX) showed price-target levels
  that looked initially surprising relative to expected share price, but each was
  double-checked by re-reading the widget's company-name/ticker confirmation line and
  confirmed to genuinely belong to the queried ticker — no substitution error, values
  recorded as-is per instructions to trust the source widget.
- No tickers required manual review; all 394 rows in the underlying analyst_targets_*.txt
  files were updated with the fresh Low/Avg/High figures.

## Full ticker list processed (394/394)

PRTA, IMVT, CCOI, AMPH, SMPL, PERI, RDNT, PENG, ATEC, NVTS, CRBU, BMEA, NSSC, VTGN, PCT.US,
INDI, FCFS, DNLI, INTA, SSYS.US, HUBG, HRMY, CORT, RYTM, KEEL, TVTX, PRCT, SHC, ZNTL, HTO,
SDA, COCO, CCC.US, CAMT, FELE, ULCC, IPAR, ATRC, CVCO, NEXT, PLRX, GGAL, MIRM, SUPN, LZ,
PSNY, MNRO, PLAB, RXST, FORM, OSIS, MYRG, SBCF, VCEL, VECO, XENE, IDYA, LAUR, TNGX, SKIN,
IMCR, REPL, GPCR, ERII, BLKB, RCKT, XMTR, IRON, WAFD, HLMN, COHU, ICFI, FULC, HURN, URGN,
VERA, CSTL, DRS, VCTR, PSMT, MGPI, XPEL, STRA, DGII, AGIO, BELFB, KRUS, RUM, JJSF, GTX.US,
AGYS, HROW, PLXS, ARHS, CENX, VNOM, ADUS, RUSHA, ARQT, MYGN, HCSG, INVZ, ECHO, EVLV, MVST,
BWIN, KYMR, BANR, BJRI, PATK, SIBN, MGEE, OCSL, ABOS, CLFD, CRNX, ANIP, TTMI, MGRC, KNSA,
TMCI, WSFS, OM.US, ROAD, POWL, GBDC, KURA, COGT, KROS, ADTN, QTRX, ESTA, INOD, REYN, HOPE,
IOSP, ADPT, SCHL, TARS, DORM, ASLE, JBSS, MBUU, OSW, SKWD, LFST, LILAK, BANF, XNCR, ECPG,
EFSC, STEP, DCGO, COLL, TCMD, NBTB, ACT, ACDC, EGBN, INVA, LMB, CMPR, FDMT, VERX, BLBD,
PRAA, APOG, MRTN, CABA, DH, LMAT, LGND, PLMR, FRME, CSWC, TRMK, RGNX, NWBI, FFBC, TIGR,
WINA, PDFS, FNKO, KALU, EYPT, MCFT, ACRS, FWRG, IMXI, ATEX, LOCO, ADEA, WABC, BCYC, SANA,
MDXG, CHCO, AMPL, MERC, AVPT, IQ.US, TFSL, HCM, ALVO, EVCM, CLBK, AFYA, GCMG, DSGR, CLBT,
HSAI, SHEN, MBIN, WALD, SRCE, TCBK, BUSE, BLTE, NRC, STBA, PEBO, TRS, ARKO, CMCO, BFC,
TRNS, QCRH, GABC, ARDX, SLRC, HSTM, SCSC, WEST, PHVS, SRRK, ASTS, CGBD, CRAI, CTBI, AVO,
PLPC, CNOB, FMBH, KELYA.US, METC, KE, IIIV, OSBC, HCKT, TCPC, BBSI, ULH, LQDT, GSBC, CCAP,
HFWA, CECO, QNST, KIDS, WVE, CCB, DMRC, OLMA, JRVR, MBWM, NAMS, OABI, CASS, UFCS, TILE,
NRDS, UVSP, IRMD, ITRN, ELVN, AMAL, LAND, RWAY, ATRO, NN, CCBG, IGIC, HNRG, GRSD, SVRA,
TYRA, BFST, TRDA, VNET, GPGI, SSP.US, SMBC, RGP, FDUS, KRNY, MSBI, ALNT, GNLX, ALEC, PAHC,
SPFI, ANTX, HAFC, DAKT, PROK, LYTS, HBNC, SENEA, FMNB, CAC, CCSI, KRT, THFF, PGC, EWTX,
IBCP, BWMN, WASH, GHRS, NAMM, BTMD, LASR, NBN, IMNM, CCNE, ESQ, NTGR, AIRS, CGEM, BTDR,
HRZN, ACTG, ORIC, AROW, ALRS, ALXO, SHBI, BHRB, SPRY, MLYS, MPB, PNTG, DSP, ACIC, LIND,
OSPN, MGNX, LUNG, ALTO, AVNW, PKOH, AURA, CGNT, JANX, NWPX.US, JBIO, BMRC, PANL, ANIK,
OKUR, CVRX, INSE, LINC, REFI, LMNR.US, ZURA, AVIR, CARE, VNDA, FISI, WLDN, CVGI, MGTX,
CBUS, LFMD, FSBW, CELC, SMTI, AUDC.US, NRIM, NECB, CLAR, NRIX, IMMR, LFCR, ASUR, CTRN,
PMTS, AIP, PRTS, GASS, OPRT, BLZE, MASS.

## Final count

394/394 processed, 394 updated, 0 flagged lost-coverage, 0 flagged for manual review.
