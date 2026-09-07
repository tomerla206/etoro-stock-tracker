# Session Log — Letter U (UAL–UVSP, 31 tickers)

- 2026-08-25: Started fresh via v4 text-based method (see PROJECT_LOG.md). Verified via `grep '^U' nasdaq_data.tsv | sort` = 31 tickers, matches expected count. No CVR tickers identified in this range. UHAL.B has a suffix, kept as-is per method.
- Reusing same browser tabs/login session verified during S1/S2/T work.
- Batch 1 done (UAL-ULBI, 10 tickers): UAL, UBSI, UCTT, UEIC, UFCS, UFPI, UFPT(NOFAQ), UHAL, UHAL.B(NOFAQ), ULBI(NOFAQ). 10/31 done. 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 3 NOFAQ. UAL correctly shows real data (140/164.86/192) — confirms Gemini's fabricated NOFAQ marking on UAL was wrong too.
- Batch 2 done (ULCC-UMBF, 4 more tickers): ULCC, ULH, ULTA, UMBF. 14/31 done. 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 3 NOFAQ.
- Batch 3 done (UNIT-UPLD, 5 more tickers): UNIT, UONE(NOFAQ), UPB, UPBD, UPLD. 19/31 done. 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 4 NOFAQ.
- Batch 4 done (UPST-URGN, 5 more tickers): UPST, UPWK, UPXI(NOFAQ), URBN, URGN. 24/31 done. 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 5 NOFAQ.
- Batch 5 done (UROY-USLM, 4 more tickers): UROY, USAR, USEA(NOT_TRADEABLE, real data), USLM(NOFAQ). 28/31 done. 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, 6 NOFAQ. Resume point: UTHR next (3 remaining: UTHR, UTMD, UVSP).
- Final batch (UTHR-UVSP, 3 more tickers): UTHR, UTMD(NOFAQ), UVSP. 31/31 DONE.
- Completeness audit (both directions vs nasdaq_data.tsv slice UAL-UVSP): clean, exact 31/31 match, 0 gaps.
- FINAL TOTALS: 31/31 tickers, 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (USEA — real data, genuinely not tradeable), 0 CVR, 7 NOFAQ (UFPT, UHAL.B, ULBI, UONE, UPXI, USLM, UTMD). No blocks this session. LETTER U COMPLETE.
