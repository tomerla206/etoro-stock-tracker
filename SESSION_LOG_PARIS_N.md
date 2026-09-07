# Session Log — Paris Group N

Continued in same session (login re-verified fresh via AAPL check at session start).

Tickers (from `paris_data.tsv`, group N = 9 tickers), in order:
1. NACON.PA — Nacon SAS — NOFAQ — price 0.0603 — TRADEABLE
2. NAE.PA — North Atlantic Energies — NOFAQ — price 79.50 — TRADEABLE
3. NANO.PA — Nanobiotix SA — TipRanks: Moderate Buy consensus, 1 analyst, Low 60.00 / Avg 60.00 / High 60.00 (OK) — price 38.420 — TRADEABLE
4. NEX.PA — Nexans SA — TipRanks: Moderate Buy consensus, 2 analysts, Low 155.00 / Avg 168.00 / High 181.00 (OK) — price 143.90 — TRADEABLE
5. NK.PA — Imerys — NOFAQ — price 24.52 — TRADEABLE
6. NOKIA.PA — Nokia Oyj — NOFAQ — price 5.5500, Market Closed — Trade button disabled=true on both checks → NOT_TRADEABLE
7. NRG.PA — NRJ Group SA — NOFAQ — price 6.42 — TRADEABLE
8. NRO.PA — Neurones SA — NOFAQ — price 37.15 — TRADEABLE
9. NXI.PA — Nexity SA — NOFAQ — price 6.815 — TRADEABLE

Result: 9/9 complete. 0 blocks. 2 OK, 7 NOFAQ. 8 TRADEABLE, 1 NOT_TRADEABLE (NOKIA.PA — the Paris-listed line of Nokia Oyj, not tradeable via this exchange listing on eToro).

Completeness audit: `grep '^N' paris_data.tsv | sort` returns exactly these 9 tickers — all present in output file, 0 gaps, 0 duplicates.

Status: DONE.
