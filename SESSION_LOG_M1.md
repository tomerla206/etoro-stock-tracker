# Session Log — Letter M1 (NASDAQ v3 combined pass)

M1 = alphabetically-first 50 of the 100 M-tickers in nasdaq_data.tsv (MAKO through MLAB inclusive). M2 (MLCO-end) is separate, not this session's job.

Worklist (50 tickers, sorted): MAKO, MAMA, MANH, MAR, MARA, MASS, MAT, MATW, MAZE, MBGL, MBIN, MBLY, MBUU, MBWM, MBX, MCBS, MCFT, MCHB, MCHP, MCRB, MCRI, MDB, MDGL, MDLN, MDLZ, MDXG, MEDP, MELI, MENS, MEOH, MERC, META, METC, METCB, MFIC, MFIN, MFP, MGEE, MGNI, MGNX, MGPI, MGRC, MGTX, MIDD.US, MIRM, MITK, MKSI, MKTW, MKTX, MLAB.

No CVR-type tickers identified in this range.

Login verified clean before starting: Tomer Lalo Schwartz, green Trade, Prices by NASDAQ, AAPL Low/Avg/High 245.00/337.09/400.00 — exact match.

**Batch 1 (13/50) done**: MAKO, MAMA, MANH, MAR, MARA, MASS, MAT, MATW, MAZE, MBGL, MBIN, MBLY, MBUU. 1 NOT_TRADEABLE (MBGL, greyed Trade button). 0 NOFAQ, 0 NEW, 0 MISMATCH so far. Two screenshot-timeout recoveries (new tab + close broken one), no blocks. Resume at MBWM.

**Batch 2 (21/50) done**: + MBWM, MBX, MCBS, MCFT, MCHB, MCHP, MCRB, MCRI. All TRADEABLE, OK. Occasional screenshot-timeout, recovered by retrying screenshot directly (tab stayed alive). No blocks. Resume at MDB.

**Batch 3 (30/50) done**: + MDB, MDGL, MDLN, MDLZ, MDXG, MEDP, MELI, MENS. All TRADEABLE/OK except MENS (NOFAQ, "This stock has no research data", NOT_TRADEABLE). No blocks. Resume at MEOH.

**Batch 4 (36/50) done**: + MEOH, MERC, META, METC, METCB, MFIC. METCB is NOFAQ but still TRADEABLE (green Trade button despite no research data). Rest OK/TRADEABLE. No blocks. Resume at MFIN.

**Batch 5 (40/50) done**: + MFIN, MFP, MGEE, MGNI. MFP is NOT_TRADEABLE (greyed Trade button) despite having OK research data. Rest OK/TRADEABLE. No blocks. Resume at MGNX.

**Batch 6 (44/50) done**: + MGNX, MGPI, MGRC, MGTX. All OK/TRADEABLE. No blocks. Resume at MIDD.US.

**Batch 7 (50/50) — M1 COMPLETE**: + MIDD.US (NOFAQ, TRADEABLE), MIRM, MITK, MKSI, MKTW (NOFAQ, TRADEABLE), MKTX, MLAB. No blocks.

**Final tally**: 50/50 tickers. 0 NEW, 0 MISMATCH. 3 NOT_TRADEABLE (MBGL, MENS, MFP). 4 NOFAQ (MENS, METCB, MIDD.US, MKTW) — of these only MENS was also NOT_TRADEABLE; METCB/MIDD.US/MKTW remained TRADEABLE despite having no research data. No CVR-type tickers in this range. No blocks/lockouts encountered this session — only recurring Claude-in-Chrome screenshot timeouts (recovered by retrying the screenshot directly, or opening a fresh tab when the old one stayed unresponsive).

**Completeness audit**: diffed the 50-ticker target list (sorted from `nasdaq_data.tsv`, MAKO through MLAB) against the final `analyst_targets_M1.txt` ticker column, both directions — zero differences. M1 confirmed complete and accurate.
