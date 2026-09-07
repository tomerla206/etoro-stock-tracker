# Session Log — NYSE Letter M2 (MMI through MYO)

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 50, sourced from `grep '^M' nyse_data.tsv`, sorted, second half (MMI through MYO). Full list:
MMI MMM MMS MNSO MNTN MO MOD MOG.A MOH MOS MOV MP MPC MPLX.US MPT MPTI MRK MRP MRSH MRTX.CVR MS MSA MSCI MSDL MSFT.24-7 MSGE MSGS MSI MSM MT.US MTB MTD MTDR MTG MTH MTN MTRN MTUS MTW MTX MTZ MUFG MUR MUSA MUX MWA MX MXL MYE MYO

**Progress**: Starting fresh 2026-08-27, immediately after letter M1 completed cleanly (50/50, no blocks, one MKC/V slash-ticker special case). Login already verified via AAPL check at session start (still valid, same browser session).

Note: MRTX.CVR is a CVR-type merger ticker — per project convention, will record directly as NOT_TRADEABLE with price from tsv, no Low/Avg/High, rather than treating as a block.

**LETTER M2 COMPLETE 2026-08-27**: 50/50 done. No blocks whatsoever.

NOFAQ (7): MMI (Marcus & Millichap), MPLX.US (MPLX LP), MPTI (M-Tron Industries), MSFT.24-7 (CFD, also NOT_TRADEABLE), MT.US (ArcelorMittal ADR), MTUS (Metallus Inc), MX (MagnaChip Semiconductor Corp). All others (42) OK/TRADEABLE.

NOT_TRADEABLE (2): MSFT.24-7 (Microsoft 24/7 CFD — Trade button both disabled, matches META.24-7/AAPL.24-7 pattern) and MRTX.CVR (Mirati Therapeutics Inc Merger CVR — verified directly via eToro, Trade button disabled, price 0.0002, recorded per project's established CVR convention with AnalysisStatus=CVR).

Completeness audit passed: 50/50 both directions against `nyse_data.tsv` (MMI through MYO), no duplicates. NYSE_LETTER_STATUS.md updated to DONE.

Both M1 and M2 (letter M, 100 tickers total) are now fully complete. Next letter per alphabetical order: N (74 tickers, not yet started).
