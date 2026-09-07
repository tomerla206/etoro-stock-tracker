# Refresh Log — Green Chunk 5

Source list: `refresh_green_chunk_05.tsv` (493 NYSE tickers, FTI through PBH).
Method: `REFRESH_METHOD.md` — TipRanks eToro widget, own dedicated Chrome tab, 15-20s randomized pacing between tickers.

## Summary

**493/493 processed, 490 updated, 3 flagged lost-coverage.**

All updated tickers had their Low/Avg/High fields (columns 4/5/6) refreshed in place in the relevant `analyst_targets_NYSE_*.txt` file. Name, Price, AnalysisStatus, and TradeStatus fields were left untouched. Files touched:

- analyst_targets_NYSE_F.txt
- analyst_targets_NYSE_G.txt
- analyst_targets_NYSE_H.txt
- analyst_targets_NYSE_I.txt
- analyst_targets_NYSE_J.txt
- analyst_targets_NYSE_K.txt
- analyst_targets_NYSE_L.txt
- analyst_targets_NYSE_M1.txt
- analyst_targets_NYSE_M2.txt
- analyst_targets_NYSE_N.txt
- analyst_targets_NYSE_O.txt
- analyst_targets_NYSE_P1.txt

## Lost coverage — flagged for manual review (left unchanged, NOT converted to NOFAQ)

- **HAFN** (Hafnia Ltd) — widget showed "This stock has no research data" (confirmed twice, no timing-related false negative).
- **KNOP** (KNOT Offshore Partners) — same, no research data.
- **MANU** (Manchester United plc) — same, no research data.

## Notes / anomalies

- Suffix stripping applied per method doc: `.US`, `.A`, `.B`, `.EUR`, trailing `/V` stripped for the query, original suffixed ticker kept as the file key (e.g. `G.US` queried as `G`, `MOG.A` queried as `MOG.A`... actually `.A` was queried as-is since TipRanks resolved it directly for MOG.A; `HEI.A` queried as `HEI` and matched HEI's own data; `LEN.B` queried as `LEN`; `MKC/V` queried as `MKC`).
- A few tickers (IP, LNC, NE, NVO, MWA) initially returned "no research data" on first navigation but this was a page-load timing artifact — re-querying after a longer wait returned full data. Only HAFN/KNOP/MANU were confirmed genuinely empty after retry.
- **FUN.US** was accidentally skipped in the main batch pass and caught afterward via a diff against the source ticker list; scraped and applied separately (Low 17.00 / Avg 23.29 / High 28.00).
- No malformed existing rows encountered requiring a fix beyond the Low/Avg/High refresh itself.
- No rate-limiting or Cloudflare issues encountered on the TipRanks widget domain, consistent with prior sessions' findings.

## Verification

Spot-checked 11 updated lines across FTI, GE, HD, IBM, JNJ, KO, LLY, MCD, NKE, O, PANW post-update — all Name/Price/Status/TradeStatus fields intact, only Low/Avg/High changed as intended.
