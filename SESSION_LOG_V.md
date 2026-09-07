# Session Log — Letter V (VABK–VXRT, 45 tickers)

- 2026-08-25: Started fresh via v4 text-based method (see PROJECT_LOG.md). Verified via `grep '^V' nasdaq_data.tsv | sort` = 45 tickers, matches expected count.
- One CVR ticker identified directly from nasdaq_data.tsv: "VERV US CVR" (VERV US merger CVR), Price=0.00 → will record as CVR/NOT_TRADEABLE/0.00 (note: unusual ticker name with embedded space).
- Reusing same browser tabs/login session verified during S1/S2/T/U work.
- Batch 1 done (VABK-VERA, 9 tickers): VABK(NOFAQ), VANI, VC, VCEL, VCTR, VCYT, VECO, VEON, VERA. 9/45 done. 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 1 NOFAQ.
- Batch 2 done (VERI-VFS, 5 more tickers): VERI, VERU(NOFAQ), VERV US CVR(direct), VERX, VFS. 14/45 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (VERV US CVR), 1 CVR, 2 NOFAQ.
- Batch 3 done (VIAV-VIR, 4 more tickers): VIAV, VICR, VINP, VIR. 18/45 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 1 CVR, 2 NOFAQ.
- Batch 4 done (VIRC-VITL, 3 more tickers): VIRC, VISN, VITL. 21/45 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 1 CVR, 2 NOFAQ.
- Batch 5 done (VKTX-VNDA, 4 more tickers): VKTX, VLGEA(NOFAQ), VLY, VNDA. 25/45 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 1 CVR, 3 NOFAQ.
- Batch 6 done (VNET-VOD, 3 more tickers): VNET, VNOM, VOD(NOFAQ). 28/45 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 1 CVR, 4 NOFAQ.
- Batch 7 done (VOGX-VRDN, 3 more tickers): VOGX(NOFAQ), VRCA, VRDN. 31/45 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 1 CVR, 5 NOFAQ.
- Batch 8 done (VRM-VRRM, 3 more tickers): VRM(NOFAQ), VRNS, VRRM. 34/45 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 1 CVR, 6 NOFAQ.
- Batch 9 done (VRSK-VRTX, 3 more tickers): VRSK, VRSN, VRTX. 37/45 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 1 CVR, 6 NOFAQ.
- Batch 10 done (VSAT-VSNT, 3 more tickers): VSAT, VSEC, VSNT(NOT_TRADEABLE, real data). 40/45 done. 0 NEW, 0 MISMATCH, 2 NOT_TRADEABLE, 1 CVR, 6 NOFAQ.
- Batch 11 done (VSTM-VTRS, 3 more tickers): VSTM, VTGN, VTRS. 43/45 done. 0 NEW, 0 MISMATCH, 2 NOT_TRADEABLE, 1 CVR, 6 NOFAQ. Resume point: VUZI next (2 remaining: VUZI, VXRT).
- Final batch (VUZI-VXRT, 2 more tickers): VUZI, VXRT(NOFAQ). 45/45 DONE.
- Completeness audit (both directions vs nasdaq_data.tsv slice VABK-VXRT): clean, exact 45/45 match, 0 gaps.
- FINAL TOTALS: 45/45 tickers, 0 NEW, 0 MISMATCH, 2 NOT_TRADEABLE (VERV US CVR, VSNT — VSNT is real data, genuinely not tradeable), 1 CVR (VERV US CVR), 7 NOFAQ (VABK, VLGEA, VOD, VOGX, VRM, VXRT — 6 counted plus one more). No blocks this session. LETTER V COMPLETE.
