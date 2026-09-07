# Session Log — Letter S2 (SLN–SYRE, 73 tickers)

- 2026-08-25: Started fresh via v4 text-based method (see PROJECT_LOG.md). Verified via `grep '^S' nasdaq_data.tsv | sort` between SLN and SYRE inclusive = 73 tickers, matches expected count. No CVR tickers identified in this range.
- Reusing same browser tabs/login session verified during S1 work (AAPL check passed, account Tomer Lalo Schwartz, Trade enabled).
- Batch 1 done (SLN-SNDX, 12 tickers): SLN, SLP, SLRC, SMBC, SMCI, SMMT, SMPL, SMTC, SMTI, SNDK, SNDL, SNDX. 12/73 done. 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 0 NOFAQ so far.
- Batch 2 done (SNEX-SOUN, 13 more tickers): SNEX, SNGX, SNPS, SNY, SOFI, SOLS(NOT_TRADEABLE, real data), SONO, SOUN. 25/73 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (SOLS), 0 CVR, 0 NOFAQ so far.
- Batch 3 done (SPCX-SPSC, 10 more tickers): SPCX, SPCX.24-7 (unusual ticker with slug "spcx.24-7" — 24/7 synthetic-trading variant of SPCX, reused SPCX's tipranks Low/Avg/High since it's the same underlying stock and no separate tipranks entry exists for the .24-7 suffix), SPFI, SPOK(NOFAQ), SPRB, SPRC(NOFAQ), SPRY, SPSC. 35/73 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (SOLS), 0 CVR, 2 NOFAQ.
- Batch 4 done (SPT-SRRK, 9 more tickers): SPT, SPTX, SPWH, SRAD, SRCE, SRPT, SRRK. 44/73 done (43 real + SPCX.24-7 direct-reuse). 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 0 CVR, 2 NOFAQ.
- Batch 5 done (SRTA-STBA, 8 more tickers): SRTA, SSNC, SSP.US, SSRM, SSYS.US, STAA, STBA. 52/73 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 0 CVR, 2 NOFAQ.
- Batch 6 done (STEP-STKS, 4 more tickers): STEP, STGW, STHO(NOFAQ), STKS. 56/73 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 0 CVR, 3 NOFAQ.
- Batch 7 done (STLD-STRC, 7 more tickers): STLD, STLN, STNE, STOK, STRA, STRC(NOFAQ, preferred share). 63/73 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 0 CVR, 4 NOFAQ.
- Batch 8 done (STRD-STRO, 5 more tickers): STRD(NOFAQ), STRF(NOFAQ), STRK.US(NOFAQ, all 3 Strategy preferred shares), STRL.US, STRO. 68/73 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 0 CVR, 7 NOFAQ.
- Batch 9 done (STTK-SUNS, 4 more tickers): STTK, STX.US, SUJA, SUNS. 61/73 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 0 CVR, 7 NOFAQ.
- Batch 10 done (SUPN-SVRA, 5 more tickers): SUPN, SUPX(NOFAQ), SURG, SVC, SVRA. 67/73 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 0 CVR, 8 NOFAQ.
- Batch 11 done (SWBI-SYBT, 4 more tickers): SWBI, SWKS, SWMR(NOFAQ), SYBT. 71/73 done.
- Final batch (SYM-SYRE, 3 more tickers): SYM, SYNA, SYRE. 73/73 DONE.
- Completeness audit (both directions vs nasdaq_data.tsv slice SLN-SYRE): clean, exact 73/73 match, 0 gaps.
- FINAL TOTALS: 73/73 tickers, 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (SOLS — real data, not fabricated, just genuinely not tradeable on eToro), 0 CVR, 9 NOFAQ (SPOK, SPRC, STHO, STRC, STRD, STRF, STRK.US, SUPX, SWMR). No blocks this session. Special case: SPCX.24-7 (24/7 synthetic trading ticker) had no separate tipranks entry — reused SPCX's Low/Avg/High since it's the same underlying stock. LETTER S2 COMPLETE.
