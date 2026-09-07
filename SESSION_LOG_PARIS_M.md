# Session Log — Paris Group M

Continued in same session (login re-verified fresh via AAPL check at session start).

Tickers (from `paris_data.tsv`, group M = 14 tickers), in order:
1. MAAT.PA — Maat Pharma SA — NOFAQ — price 3.04 — TRADEABLE
2. MAU.PA — Etablissements Maurel & Prom SA — NOFAQ — price 7.900 — TRADEABLE
3. MBWS.PA — Marie Brizard Wine and Spirits SA — NOFAQ — price 2.980 — TRADEABLE
4. MC.PA — LVMH Moet Hennessy Louis Vuitton SA — TipRanks: Moderate Buy consensus, 7 analysts, Low 510.00 / Avg 578.43 / High 645.00 (OK) — price 458.35 — TRADEABLE
5. MDM.PA — Maisons du Monde SA — NOFAQ — price 0.219 — TRADEABLE
6. MEDCL.PA — Medincell SA — TipRanks: Moderate Buy consensus, 1 analyst, Low 38.00 / Avg 38.00 / High 38.00 (OK) — price 24.64 — TRADEABLE
7. MEMS.PA — Memscap SA — NOFAQ — price 4.830 — TRADEABLE
8. MERY.PA — Mercialys — TipRanks: Hold consensus, 1 analyst, Low 12.50 / Avg 12.50 / High 12.50 (OK) — price 11.080 — TRADEABLE
9. MF.PA — Wendel — TipRanks: Moderate Buy consensus, 1 analyst, Low 115.00 / Avg 115.00 / High 115.00 (OK) — price 86.70 — TRADEABLE
10. ML.PA — Compagnie Generale DES Etablissements Michelin SCA — TipRanks: Moderate Buy consensus, 3 analysts, Low 37.00 / Avg 38.50 / High 40.00 (OK) — price 34.720 — TRADEABLE
11. MMB.PA — Lagardere SCA — NOFAQ — price 18.86 — TRADEABLE
12. MMT.PA — Metropole Television SA — NOFAQ — price 11.88 — TRADEABLE
13. MRN.PA — Mersen SA — TipRanks: Moderate Buy consensus, 2 analysts, Low 50.00 / Avg 51.50 / High 53.00 (OK) — price 38.50 — TRADEABLE
14. MTU.PA — Manitou BF SA — NOFAQ — price 21.05 — TRADEABLE

Result: 14/14 complete. 0 blocks. 6 OK, 8 NOFAQ. All 14 TRADEABLE.

Completeness audit: `grep '^M' paris_data.tsv | sort` returns exactly these 14 tickers — all present in output file, 0 gaps, 0 duplicates.

Status: DONE.
