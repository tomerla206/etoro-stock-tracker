# Session Log — NYSE Letter K

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 46, sourced from `grep '^K' nyse_data.tsv`, sorted. Full list:
KAI KB KBH KBR KD KDK KEN KEP KEX KEY KEYS KFRC KFY KGC KGS.US KIM KKR KLAR KLC KMI KMPR KMT KMX KN KNF KNOP KNTK KNX KO KODK.US KOF KOP KOS KR KRC KREF KRG KRMN KRO KSS KT KTB KVUE KVYO KWR KWY

**Progress**: Starting fresh 2026-08-27, right after letter J completed cleanly (20/20, no blocks).

**Checkpoint 2026-08-27**: 12/46 done (through KFRC). No blocks. NOFAQ so far: KEN, KEP. All others OK/TRADEABLE. Next: KFY.

**Checkpoint 2 2026-08-27**: 24/46 done (through KN). No blocks. All this stretch (KFY, KGC, KGS.US, KIM, KKR, KLAR, KLC, KMI, KMPR, KMT, KMX, KN) came back OK/TRADEABLE, no new NOFAQ. Next: KNF.

**Checkpoint 3 2026-08-27**: 34/46 done (through KR). No blocks. New NOFAQ: KODK.US (Eastman Kodak). All others this stretch (KNF, KNOP, KNTK, KNX, KO, KOF, KOP, KOS, KR) OK/TRADEABLE. Next: KRC.

**Checkpoint 4 2026-08-27**: 40/46 done (through KSS). No blocks. All this stretch (KRC, KREF, KRG, KRMN, KRO, KSS) OK/TRADEABLE. Remaining: KT, KTB, KVUE, KVYO, KWR, KWY.

**LETTER K COMPLETE 2026-08-27**: 46/46 done. No blocks whatsoever this entire letter. Final NOFAQ list: KEN, KEP, KODK.US (Eastman Kodak), KT (KT Corporation), KWY (Kingsway Corp) — 5 total. All others OK/TRADEABLE. No CVR tickers in this letter. Completeness audit passed: 46/46 both directions, no duplicates. NYSE_LETTER_STATUS.md updated to DONE. Next letter: L (58 tickers, not yet started).
