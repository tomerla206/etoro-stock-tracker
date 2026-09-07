# Session Log — Frankfurt Letter M

2026-08-28: Started immediately after letter L completed (same session, strict sequential mode). Note: 32 tickers, large letter — working straight through sequentially (not split into M1/M2 as some other exchanges did).

Batch 1 (6/32): M12.DE (NOFAQ), M3B0.DE (NOFAQ), M3V.DE (NOFAQ), M5S.DE (NOFAQ), M5Z.DE (NOFAQ), M7U.DE (NOFAQ) — zero blocks. One transient "Claude in Chrome is not connected" hiccup after M5Z.DE — retried tabs_context_mcp, connection was back immediately, no data lost, continued normally.

Tally at 6/32: 0 OK, 6 NOFAQ, 0 NOT_TRADEABLE, 0 CVR/MISMATCH.

Remaining (26): MA10.DE, MAK.DE, MBB.DE, MBG.DE, MBK.DE, MBQ.DE, MDG1.DE, MED.DE, META.EUR, MLL.DE, MLP.DE, MPCK.DE, MRK.DE, MRX.DE, MSAG.DE, MSFT.EUR, MTX.DE, MUB.DE, MUM.DE, MUV2.DE, MUX.DE, MVV1.DE, MWB0.DE, MXHN.DE, MYM.DE, MZX.DE.

Batch 2 (13/32 total): MA10.DE (NOFAQ), MAK.DE (NOFAQ), MBB.DE (OK), MBG.DE (OK), MBK.DE (NOFAQ), MBQ.DE (NOFAQ), MDG1.DE (NOFAQ, NOT_TRADEABLE — Trade button disabled:true x2) — zero blocks.

Tally at 13/32: 3 OK, 9 NOFAQ, 1 NOT_TRADEABLE, 0 CVR/MISMATCH.

Remaining (19): MED.DE, META.EUR, MLL.DE, MLP.DE, MPCK.DE, MRK.DE, MRX.DE, MSAG.DE, MSFT.EUR, MTX.DE, MUB.DE, MUM.DE, MUV2.DE, MUX.DE, MVV1.DE, MWB0.DE, MXHN.DE, MYM.DE, MZX.DE.

Batch 3 (19/32 total): MED.DE (NOFAQ), META.EUR (OK — confirmed tipranks widget needs bare "META" not "META.EUR", eToro slug meta.eur worked directly), MLL.DE (NOFAQ), MLP.DE (OK), MPCK.DE (NOFAQ), MRK.DE (OK) — zero blocks.

Tally at 19/32: 6 OK, 12 NOFAQ, 1 NOT_TRADEABLE, 0 CVR/MISMATCH.

Remaining (13): MRX.DE, MSAG.DE, MSFT.EUR, MTX.DE, MUB.DE, MUM.DE, MUV2.DE, MUX.DE, MVV1.DE, MWB0.DE, MXHN.DE, MYM.DE, MZX.DE.

Batch 4 (25/32 total): MRX.DE (NOFAQ), MSAG.DE (NOFAQ), MSFT.EUR (OK — same pattern as META.EUR, tipranks widget wants bare "MSFT"), MTX.DE (OK), MUB.DE (NOFAQ), MUM.DE (NOFAQ) — zero blocks.

Tally at 25/32: 9 OK, 15 NOFAQ, 1 NOT_TRADEABLE, 0 CVR/MISMATCH.

Remaining (7): MUV2.DE, MUX.DE, MVV1.DE, MWB0.DE, MXHN.DE, MYM.DE, MZX.DE.

**LETTER M COMPLETE (32/32), 2026-08-28.** Finished remaining 7: MUV2.DE (OK), MUX.DE (OK), MVV1.DE (NOFAQ), MWB0.DE (NOFAQ), MXHN.DE (NOFAQ), MYM.DE (NOFAQ), MZX.DE (NOFAQ). Zero blocks entire letter (one transient Chrome-extension disconnect early on, recovered immediately with no data loss).

Final tally (32/32): 11 OK, 20 NOFAQ, 1 NOT_TRADEABLE (MDG1.DE), 0 CVR/MISMATCH.

Completeness audit: 0 gaps, 0 extras vs `grep '^M' frankfurt_data.tsv`. PASSED.
