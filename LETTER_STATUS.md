# Letter Claim Board — NASDAQ v3 Combined Pass

**Read `PROJECT_LOG.md` first** — it has the full method, mandatory pacing protocol, and block-handling rules. This file is just the live status board. Full incident-by-incident history for any letter lives in that letter's own `SESSION_LOG_<LETTER>.md` — this table only keeps a one-line summary per letter to stay fast to read.

**⚠️ One active agent at a time, across NASDAQ + NYSE combined** — check `NYSE_LETTER_STATUS.md` too before claiming.

## Claim table

| Letter | Ticker count | Status | Notes |
|---|---|---|---|
| A | 191 | **DONE — 191/191** | 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE, ~21 NOFAQ. See `SESSION_LOG_A.md`. |
| B | 85 | **DONE — 85/85** | 0 NEW, 0 MISMATCH, 3 NOT_TRADEABLE (BBBYW, BOXL, BTTC), 20 NOFAQ. See `SESSION_LOG_B.md`. |
| C | 171 | **DONE — 171/171** | 0 NEW, 0 MISMATCH, 2 NOT_TRADEABLE (CDT, CLRS), 4 CVR, 23 NOFAQ. Completeness audit caught 3 earlier-skipped tickers (CDNS, CRMD, CRWV). See `SESSION_LOG_C.md`. |
| D | 48 | **DONE — 48/48** | 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 6 NOFAQ. See `SESSION_LOG_D.md`. |
| E | 59 | **DONE — 59/59** | 0 NEW, 0 MISMATCH, 5 NOT_TRADEABLE (incl. 3 CVR), 9 NOFAQ. See `SESSION_LOG_E.md`. |
| F | 77 | **DONE — 77/77** | 0 NEW, 0 MISMATCH, 3 NOT_TRADEABLE (FFAI, FRMM, FUSN.CVR), 14 NOFAQ. See `SESSION_LOG_F.md`. |
| G | 69 | **DONE — 69/69** | 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (GDHG), 0 CVR, 14 NOFAQ. Completeness audit (both directions vs `nasdaq_data.tsv`) clean — also caught and recovered GIX (GigCapital9 Corp), which had been missing from the original worklist entirely. No lockout this session. See `SESSION_LOG_G.md`. |
| H | 62 | **DONE — 62/62** | 0 NEW, 0 MISMATCH, 2 NOT_TRADEABLE (HOLO, HYZN), 2 CVR, 13 NOFAQ (HEPS, HIFS, HOFT, HOLO, HOVR, HOWL, HPAI, HPK, HRTX, HSPOF, HWH, HYFM, HYZN). Two lockouts this letter (blocked on HLIT then HUT), both cleared via re-login/router-toggle recovery, no data lost. Completeness audit clean, both directions. See `SESSION_LOG_H.md`. |
| I | 83 | **DONE — 83/83** | 0 NEW, 0 MISMATCH, 2 NOT_TRADEABLE (INBX, INHD), 1 CVR (INBX.CVR), 15 NOFAQ. Completeness audit (both directions vs `nasdaq_data.tsv`) clean. One prior lockout (on IMMX) cleared via re-login, no data lost. See `SESSION_LOG_I.md`. |
| J | 18 | **DONE — 18/18** | 0 NEW, 0 MISMATCH, 2 NOT_TRADEABLE (JAGX, JAGX.PFD), 3 NOFAQ (JD.US, JFU, JOUT — all still TRADEABLE despite no research data). Completeness audit (both directions vs `nasdaq_data.tsv`) clean. No blocks this session. See `SESSION_LOG_J.md`. |
| K | 36 | **DONE — 36/36** | 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (KUST), 0 CVR, 6 NOFAQ (KUST, KNDI, KELYA.US, KLXE, KIDZ, KALA — all TRADEABLE except KUST). Completeness audit (both directions vs `nasdaq_data.tsv`) clean. No blocks this session. See `SESSION_LOG_K.md`. |
| L | 82 | **DONE — 82/82** | 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 0 CVR, 19 NOFAQ. CAPTCHA block from a prior session had cleared on its own by resume time. Completeness audit (both directions vs `nasdaq_data.tsv`) clean. See `SESSION_LOG_L.md`. |
| M1 | 50 | **DONE — 50/50** | First half of M (MAKO-MLAB alphabetically). 0 NEW, 0 MISMATCH, 3 NOT_TRADEABLE (MBGL, MENS, MFP), 4 NOFAQ (MENS, METCB, MIDD.US, MKTW — METCB/MIDD.US/MKTW still TRADEABLE despite no research data). Completeness audit (both directions vs `nasdaq_data.tsv`) clean. No blocks. See `SESSION_LOG_M1.md`. |
| M2 | 50 | **DONE — 50/50** | Second half of M (MLCO-end alphabetically). 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (MLGO), 1 CVR (MRSN CVR), 10 NOFAQ (of which only MLGO also NOT_TRADEABLE). Completeness audit (both directions vs `nasdaq_data.tsv`) clean. No blocks. See `SESSION_LOG_M2.md`. |
| N | 84 | **DONE — 84/84** | 0 NEW, 0 MISMATCH, 4 NOT_TRADEABLE (NAAS, NBEVQ, NSTGQ CVR-Escrow, NUWE), 1 CVR (NSTGQ CVR-Escrow), 21 NOFAQ. Completeness audit (both directions vs `nasdaq_data.tsv`) clean. One ordinary lockout from a prior session (on NEGG) cleared via re-login before this session started; no blocks during this session's work. See `SESSION_LOG_N.md`. |
| O | 58 | **DONE — 58/58** | 0 NEW, 0 MISMATCH, 4 NOT_TRADEABLE (OPENL, OPENW, OPENZ Opendoor warrants, OZON), 0 CVR, 15 NOFAQ. Completeness audit (both directions vs `nasdaq_data.tsv`) clean. Two ordinary lockouts this letter (OPRA, OXSQ), both cleared via genuine user re-login, no data lost. See `SESSION_LOG_O.md`. |
| P1 | 53 | **DONE — 53/53** | 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 0 CVR, 8 NOFAQ (PAHC, PAX, PCT.US, PCYO, PDLB, PETS.US, PFIS, PHUN — all still TRADEABLE). Completeness audit (both directions vs the 53-ticker P1 list) clean. One ordinary lockout from a prior session (on PGY) cleared via re-login before this session's resume; no blocks during this session's work. See `SESSION_LOG_P1.md`. |
| P2 | 54 | **DONE — 54/54** | 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (PSTX.CVR), 1 CVR (PSTX.CVR), 6 NOFAQ. Completeness audit (both directions vs `nasdaq_data.tsv`) clean. Two ordinary lockouts this letter (PRCT, PTRN), both cleared via user power-cycle/re-login, no data lost. See `SESSION_LOG_P2.md`. |
| Q | 16 | **DONE — 16/16** | 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (QIWI), 0 CVR, 2 NOFAQ (QIWI, QNT.US — QNT.US still TRADEABLE). One ordinary lockout from a prior session (on QTRX) cleared via re-login; no blocks during this session's final 4 tickers. Completeness audit (both directions vs `nasdaq_data.tsv`) clean. See `SESSION_LOG_Q.md`. |
| R | 78 | **DONE — 78/78** | Completed 78/78 tickers. See `SESSION_LOG_R.md`. |
| S1 | 72 | **DONE — 72/72** | First half of S (SABR-SLMT alphabetically). 0 NEW, 0 MISMATCH, 4 NOT_TRADEABLE (SAGE CVR, SCLX, SCPH CVR, SFTGQ), 2 CVR, 10 NOFAQ. v4 text-based method (see PROJECT_LOG.md) worked cleanly, no blocks. Completeness audit clean both directions. See `SESSION_LOG_S1.md`. |
| S2 | 73 | **DONE — 73/73** | Second half of S (SLN-SYRE alphabetically). 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (SOLS), 0 CVR, 9 NOFAQ. v4 method, no blocks. Completeness audit clean both directions. See `SESSION_LOG_S2.md`. |
| T | 91 | **DONE — 91/91** | 0 NEW, 0 MISMATCH, 5 NOT_TRADEABLE (TECX.CVR, THRD, TKVA, TRAX, TSLA.24-7), 1 CVR, 14 NOFAQ. v4 method, no blocks. Completeness audit clean both directions. See `SESSION_LOG_T.md`. |
| U | 31 | **DONE — 31/31** | 0 NEW, 0 MISMATCH, 1 NOT_TRADEABLE (USEA), 0 CVR, 7 NOFAQ. v4 method, no blocks. Completeness audit clean both directions. See `SESSION_LOG_U.md`. |
| V | 45 | **DONE — 45/45** | 0 NEW, 0 MISMATCH, 2 NOT_TRADEABLE (VERV US CVR, VSNT), 1 CVR, 7 NOFAQ. v4 method, no blocks. Completeness audit clean both directions. See `SESSION_LOG_V.md`. |
| W | 50 | **DONE — 50/50** | 0 NEW, 0 MISMATCH, 3 NOT_TRADEABLE (WBA US CVR, WIMI, WKHS), 1 CVR (WBA US CVR), 9 NOFAQ. v4 method, no blocks. Completeness audit clean both directions. See `SESSION_LOG_W.md`. |
| X | 20 | **DONE — 20/20** | Completed 20/20 tickers. See `SESSION_LOG_X.md`. |
| Y | 2 | **DONE — 2/2** | 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 0 CVR, 1 NOFAQ (YORW.US, still TRADEABLE). Completeness audit (both directions vs `nasdaq_data.tsv`) clean. No blocks. Confirmed dual-agent tab cross-talk with the parallel R-letter forward agent on the auto-created tab; resolved by creating a dedicated second tab (per known fix), no data lost. See `SESSION_LOG_Y.md`. |
| Z | 15 | **DONE — 15/15** | 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 0 CVR, 2 NOFAQ (ZJYL, ZUMZ — both still TRADEABLE). Completeness audit (both directions vs `nasdaq_data.tsv`) clean. Prior ordinary lockout on ZURA cleared via re-login; resumed on a dedicated new tab after finding the original tab was being actively shared/driven by the parallel forward (Q) agent. No blocks during resumption. See `SESSION_LOG_Z.md`. |

Total baseline: 1823 tickers (`nasdaq_data.tsv`, confirmed complete via TABON cross-check — see `PROJECT_HISTORY.md` if you need that story).

## Claiming a letter

1. Confirm no other agent is active (this board + `NYSE_LETTER_STATUS.md`).
2. Set Status → `IN PROGRESS`, save immediately.
3. If old `analyst_targets_<LETTER>.txt` data exists but predates the v3 method (8-column format with `TradeStatus`), back it up to `analyst_targets_<LETTER>_OLD_tipranks_method.txt` and start clean — v2 data isn't reusable.
4. Work per `PROJECT_LOG.md`'s method + mandatory pacing protocol.
5. Update this row's Status/Notes at every checkpoint, not just at the end.

## Merging (do only when the user asks, once several letters are DONE)

See `PROJECT_LOG.md`'s "Key files" section for `merge_analyst_targets.py`'s usage — read every `analyst_targets_*.txt`, patch `nasdaq_rows.html`, reassemble `nasdaq-stocks.html`, republish to the existing artifact URL.
