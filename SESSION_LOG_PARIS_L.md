# Session Log — Paris Group L

Continued in same session (login re-verified fresh via AAPL check at session start).

Tickers (from `paris_data.tsv`, group L = 11 tickers), in order:
1. LACR.PA — Lacroix Group SA — NOFAQ — price 17.20 — TRADEABLE
2. LAT.PA — Latecoere SA — NOFAQ — price 0.0145 — TRADEABLE
3. LBIRD.PA — Lumibird SA — NOFAQ — price 25.30 — TRADEABLE
4. LHYFE.PA — Lhyfe SA — NOFAQ — price 2.135 — TRADEABLE
5. LI.PA — Klepierre SA — TipRanks: Hold consensus, 1 analyst, Low 39.00 / Avg 39.00 / High 39.00 (OK) — price 37.88 — TRADEABLE
6. LIN.PA — Linedata Services SA — NOFAQ — price 44.40 — TRADEABLE
7. LNA.PA — LNA Sante SA — NOFAQ — price 33.80 — TRADEABLE
8. LPE.PA — Laurent Perrier SA — NOFAQ — price 81.00 — TRADEABLE
9. LR.PA — Legrand SA — TipRanks: Moderate Buy consensus, 2 analysts, Low 160.00 / Avg 180.00 / High 200.00 (OK) — price 140.25 — TRADEABLE
10. LSS.PA — Lectra SA — NOFAQ — price 22.60 — TRADEABLE
11. LTA.PA — Altamir SCA — NOFAQ — price 23.10 — Trade button disabled=true on both checks → NOT_TRADEABLE

Result: 11/11 complete. 0 blocks. 2 OK, 9 NOFAQ. 10 TRADEABLE, 1 NOT_TRADEABLE (LTA.PA).

Completeness audit: `grep '^L' paris_data.tsv | sort` returns exactly these 11 tickers — all present in output file, 0 gaps, 0 duplicates.

Status: DONE.
