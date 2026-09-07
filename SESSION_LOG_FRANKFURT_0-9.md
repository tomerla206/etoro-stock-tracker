# Session Log — Frankfurt group 0-9

2026-08-26: Own dedicated Chrome tab created (tabId 1160639712) per dual-agent parallel-run policy — never touched the other tab that appeared in the group (1160639718, seen navigating French/Paris tickers like AB.PA/ABCA.PA/ABEO.PA/ABNX.PA/ABVX.PA — clearly a different, unrelated agent, left alone throughout).

Login verified via AAPL check: real-time price 309.41 (Off-hours, not "Delayed"), "Prices by NASDAQ, in USD", Trade button green/disabled:false, Low/Avg/High 245/337.09/400 all present. Logged in as Tomer Lalo Schwartz. Clear to proceed.

Worked all 14 digit-leading tickers in one pass (small group, no batch-pause needed), v4 method, randomized 2-7s waits between navigations:

- 0B2.DE (BAWAG Group AG) — 178.50, Low 191.00 / Avg 193.67 / High 198.00, OK, TRADEABLE
- 1FC.DE (FACC AG) — 15.120, NOFAQ, TRADEABLE
- 1GBS.DE (GBS Software AG) — 4.28, NOFAQ, TRADEABLE
- 1SXP.DE (SCHOTT Pharma AG & Co KgaA) — 23.35, NOFAQ, TRADEABLE
- 1U1.DE (1&1 AG) — 22.50, Low 24.00 / Avg 25.60 / High 27.00, OK, TRADEABLE
- 22UA.DE (Biontech SE) — 98.00, Low 98.54 / Avg 112.00 / High 121.68, OK, TRADEABLE
- 2HRA.DE (H&R GmbH & Co KgaA) — 6.30, NOFAQ, TRADEABLE
- 2INV.DE (2Invest AG) — 7.94, NOFAQ, TRADEABLE
- 2M6.DE (Medtronic PLC) — 77.90, Low 71.12 / Avg 80.55 / High 89.97, OK, TRADEABLE
- 3SQ1.DE (AHT Syngas Technology NV) — 2.42, NOFAQ, TRADEABLE
- 4DS.DE (Daldrup & Soehne AG) — 21.70, NOFAQ, TRADEABLE
- 690D.DE (Haier Smart Home Co Ltd) — 1.7940, NOFAQ, TRADEABLE
- 8TRA.DE (TRATON SE) — 38.14, Low 35.00 / Avg 38.50 / High 43.00, OK, TRADEABLE
- 93M1.DE (MPH Health Care AG) — 24.70, NOFAQ, TRADEABLE

No blocks hit. No CVR-equivalent tickers found (none of the 14 had 0.00 price or delisted/merger-escrow markers).

Completeness audit: diffed all 14 digit-leading tickers in `frankfurt_data.tsv` against `analyst_targets_FRANKFURT_0-9.txt` output, both directions — exact match, 14/14, 0 missing, 0 extra.

**Group 0-9: DONE.** 6 OK / 8 NOFAQ / 0 NOT_TRADEABLE / 0 CVR / 0 blocks.

Moving on to letter A next (39 tickers), per instructions to continue automatically.
