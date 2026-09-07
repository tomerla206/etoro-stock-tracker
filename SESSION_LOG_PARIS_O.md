# Session Log — Paris Group O

Continued in same session (login re-verified fresh via AAPL check at session start).

Tickers (from `paris_data.tsv`, group O = 5 tickers), in order:
1. ODET.PA — Compagnie de lOdet — NOFAQ — price 1320.00 — TRADEABLE
2. OPM.PA — Opmobility — TipRanks: Moderate Buy consensus, 2 analysts, Low 16.50 / Avg 17.25 / High 18.00 (OK) — price 12.660 — TRADEABLE
3. OR.PA — LOreal SA — TipRanks: Moderate Buy consensus, 2 analysts, Low 390.00 / Avg 420.00 / High 450.00 (OK) — price 387.80 — TRADEABLE
4. ORA.PA — Orange — TipRanks: Strong Buy consensus, 4 analysts, Low 17.00 / Avg 19.67 / High 21.80 (OK) — price 14.950 — TRADEABLE
5. OSE.PA — OSE Immunotherapeutics SA — NOFAQ — price 3.252 — TRADEABLE

Result: 5/5 complete. 0 blocks. 3 OK, 2 NOFAQ. All 5 TRADEABLE.

Completeness audit: `grep '^O' paris_data.tsv | sort` returns exactly these 5 tickers — all present in output file, 0 gaps, 0 duplicates.

Status: DONE.
