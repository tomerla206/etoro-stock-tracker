# Session Log — NYSE Letter C2 (CNP through CYH)

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 79, sourced from `grep '^C' nyse_data.tsv`, sorted, second half (C2). Full list:
CNP CNQ CNR CNS CNX CODI COF COHR COLD COMP.US CON.US COOK COP COR COTY COUR CP CPA CPAY CPF CPK CPNG CPRI CPS CPT CQP CR CRBG CRC CRCL CRD.A CRGY CRH CRI CRK CRL CRM CRS CSAN CSL CSQR CSR CSTM CSV CSW CTEV CTGO CTO CTOS CTRE CTRI CTS CTVA CUBE CUBI CURB CURV CUZ CVE CVEO CVI.US CVLG CVM CVNA CVR.THS CVS CVSA CVX.US CW CWEN CWH CWK.US CWT CX CXM CXT CXW CYD CYH

**Progress**: 79/79 DONE. Completed 2026-08-27, resumed cleanly with freshly-verified eToro login (AAPL confirmed real-time). No blocks the entire session. Completeness audit passed (79/79, both directions, no duplicates).

Session 2026-08-27: CPRI through CYH all fetched. NOFAQ: CSAN, CTS, CVM (3). CVR-type: CVR.THS (1, recorded directly without site visit per method). All others OK/TRADEABLE. CVI.US and CVX.US required the plain ticker (no .US suffix) on the tipranks widget URL — the .US suffix returned a false NOFAQ on tipranks (eToro-side URL still needs the suffix).
