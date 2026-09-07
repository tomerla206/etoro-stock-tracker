# Session Log — NYSE Letter M1 (M.US through MLR)

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 50, sourced from `grep '^M' nyse_data.tsv`, sorted, first 50 (M.US through MLR). Full list:
M.US MA MAA MAC MAGN MAIN MAIR MAN MANE MANU MAS MATV MATX MAX MBC MBI MC MCB MCD MCK MCO MCS.US MCY MD MDT.US MDU MEC MED.US MEI MET.US META.24-7 MFA MFC MFG MG MGA MGM MGY MH MHK MHO MIAX MICC.US MIR.US MKC MKC/V MKL MLI MLM MLR

**Progress**: Starting fresh 2026-08-27, right after letter L completed cleanly (58/58, no blocks). M split into M1 (M.US-MLR, this file) and M2 (MMI-MYO) since M has 100 tickers total.

**LETTER M1 COMPLETE 2026-08-27**: 50/50 done. No blocks whatsoever. Login verified via AAPL check (real price 310.12, "Prices by NASDAQ" not delayed, Trade button enabled) before starting.

NOFAQ (14): M.US (Macy's), MATV (Mativ Holdings), MCS.US (Marcus Corp), MCY (Mercury General), MDT.US (Medtronic), MED.US (Medifast), MET.US (Metlife), META.24-7 (CFD, also NOT_TRADEABLE), MFG (Mizuho Financial), MG (Mistras Group), MICC.US (Magnum Ice Cream Co BV), MIR.US (Mirion Technologies), MKC/V (McCormick & Co Inc/MD), MLI (Mueller Industries). All others (36) OK/TRADEABLE.

NOT_TRADEABLE (1): META.24-7 (Meta 24/7 CFD — Trade button both disabled, matches AAPL.24-7/AMZN.24-7 pattern from letter A).

Special case: MKC/V (McCormick & Co Inc/MD) — eToro's `/markets/mkc-v` and `/markets/mkc.v` URL variants both redirect to home (routing quirk with the slash in ticker), and the in-app search box was unreliable for automated interaction this session (dropdown intermittently failed to render/respond to clicks). Confirmed via eToro's own search-dropdown screenshot that MKC/V is listed as "Stocks, NYSE" with an enabled green Trade button (same visual style as confirmed-tradeable MKC) — recorded as TRADEABLE on that basis. Analyst data (NOFAQ) confirmed directly via tipranks widget using the literal ticker `MKC/V` as a query param (works fine there, no routing issue). Price 55.53 taken from `nyse_data.tsv` since the precise eToro price page wasn't reachable — same convention as other precedent cases in this project (e.g. IR/TT in letter I) where an eToro routing quirk required an alternate confirmation path rather than being treated as a block.

Correction note: MKL (Markel Corp) was initially fetched with a data error during a batch of tool-connectivity hiccups (tab got stuck loading) — caught before finalizing and re-fetched correctly: price 1815.57, Low/Avg/High all 1950.00 (2 analysts), OK/TRADEABLE. Verified correct in final file.

Completeness audit passed: 50/50 both directions against `nyse_data.tsv` (M.US through MLR), no duplicates. NYSE_LETTER_STATUS.md updated to DONE. Moving on to M2 (MMI-MYO, 50 tickers) next, per standing instructions.
