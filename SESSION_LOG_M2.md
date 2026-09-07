# Session Log — Letter M2 (NASDAQ v3 combined pass)

M2 = alphabetically-second 50 of the 100 M-tickers in nasdaq_data.tsv (MLCO through MZTI inclusive). M1 (MAKO-MLAB) already done.

Worklist (50 tickers, sorted): MLCO, MLGO, MLKN, MLTX, MLYS, MMED, MMSI, MMYT, MNDY, MNKD, MNRO, MNST, MNTK, MNY, MOBI, MOMO, MORN, MPAA, MPB, MPWR, MQ, MRAM, MRCY, MREO, MRNA, MRSN CVR, MRTN, MRVI, MRVL, MRX, MSBI, MSEX, MSFT, MSPR, MSTR, MTC, MTCH, MTLS, MTRX, MTSI, MU, MVBF, MVIS, MVST, MWC, MWH, MYGN, MYPS, MYRG, MZTI.

"MRSN CVR" identified as CVR-type ticker (name "MRSN Merger CVR", price 0.00 in tsv) — will be recorded directly as CVR/NOT_TRADEABLE/0.00 without visiting eToro, per protocol.

Login verified clean before starting: Tomer Lalo Schwartz, green Trade, Prices by NASDAQ, AAPL Low/Avg/High 245.00/337.09/400.00 — exact match.

**Batch 1 (13/50) done**: MLCO, MLGO, MLKN, MLTX, MLYS, MMED, MMSI, MMYT, MNDY, MNKD, MNRO, MNST, MNTK. 1 NOT_TRADEABLE (MLGO, greyed Trade, NOFAQ). 2 more NOFAQ but still TRADEABLE (MLKN, MNTK). Rest OK/TRADEABLE. Several screenshot-timeout recoveries (new tab + close broken one) especially early on; switched to plain full-page `screenshot` instead of `zoom` after timeouts kept recurring on `zoom` calls — screenshots at 1568x784 are clearly readable and more reliable. No blocks. Resume at MNY.

**Batch 2 (26/50) done**: + MNY, MOBI, MOMO, MORN, MPAA, MPB, MPWR, MQ, MRAM, MRCY, MREO, MRNA, MRSN CVR. MRSN CVR recorded directly (CVR/NOT_TRADEABLE/0.00) without visiting eToro per protocol. 2 NOFAQ but TRADEABLE (MNY, MOMO). Rest OK/TRADEABLE. No blocks, no screenshot timeouts this batch (single-screenshot-per-nav pattern holding up well on the same tab). Resume at MRTN.

**Batch 3 (39/50) done**: + MRTN, MRVI, MRVL, MRX, MSBI, MSEX, MSFT, MSPR, MSTR, MTC, MTCH, MTLS, MTRX. 0 NOT_TRADEABLE. 4 NOFAQ but TRADEABLE (MSPR — note: shows "Prices by OTC Markets" not NASDAQ but still green Trade, MTC, MTLS). Rest OK/TRADEABLE. No blocks. Same tab held up for entire batch (13 navigations), no screenshot timeouts. Resume at MTSI.

**Batch 4 (50/50) — M2 COMPLETE**: + MTSI, MU, MVBF, MVIS, MVST, MWC, MWH, MYGN, MYPS, MYRG, MZTI. All OK/TRADEABLE except 3 more NOFAQ-but-TRADEABLE (MVIS, MWC, MYPS). No blocks.

**Final tally**: 50/50 tickers. 0 NEW, 0 MISMATCH. 1 NOT_TRADEABLE (MLGO, NOFAQ + greyed Trade). 1 CVR (MRSN CVR, recorded directly per protocol). 10 NOFAQ total (MLGO, MLKN, MNTK, MNY, MOMO, MSPR, MTC, MTLS, MVIS, MWC, MYPS — note that's 11, MLGO counted once as both NOT_TRADEABLE and NOFAQ) — of these only MLGO was also NOT_TRADEABLE; the rest remained TRADEABLE despite no research data. No blocks/lockouts encountered this session. Login verified clean at start (Tomer Lalo Schwartz, green Trade, Prices by NASDAQ, AAPL 245.00/337.09/400.00 exact match).

**Technique note**: `zoom` calls started timing out (CDP screenshot capture) after only a few uses per tab early in the session; switched to plain full-page `screenshot` (1568x784, clearly readable) which proved far more reliable — one tab held up for 24 consecutive ticker navigations (batches 3+4) without a single timeout using this approach.

**Completeness audit**: diffed the 50-ticker target list (sorted from `nasdaq_data.tsv`, MLCO through MZTI) against the final `analyst_targets_M2.txt` ticker column, both directions — zero differences. M2 confirmed complete and accurate.
