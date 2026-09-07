# Sydney (ASX) Letter Claim Board — v4 Combined eToro Analysis-Tab Pass

## *** SYDNEY EXCHANGE 100% COMPLETE — 221/221 TICKERS — 2026-08-28 ***

All 24 letters (A-T, V-Y; no U or Z tickers present in `sydney_data.tsv`) are done. Full-exchange completeness audit (all `analyst_targets_SYDNEY_*.txt` concatenated vs. full `sydney_data.tsv` ticker list) passed with **zero diff**. Zero unresolved blocks across the entire exchange. See `SESSION_LOG_SYDNEY_Y.md` for the final-letter summary and full-exchange audit note. **Project queue moves to Stockholm next.**

**Read `SYDNEY_PROJECT_LOG.md` first.** Runs in parallel with NYSE, Frankfurt, and Paris by explicit user decision 2026-08-26.

## Ticker counts per letter (from `sydney_data.tsv`, built 2026-08-26, 221 tickers total, 0 duplicates)

| Letter | Ticker count | Status | Claimed by | Output file | Notes |
|---|---|---|---|---|---|
| A | 23 | **DONE (23/23)** | background agent | `analyst_targets_SYDNEY_A.txt` | Complete 2026-08-28. AZJ.ASX redone fresh, no block this time. Completeness audit passed (zero gaps vs sydney_data.tsv). 22 TRADEABLE, 1 NOT_TRADEABLE (ALU.ASX), 0 NOFAQ. See `SESSION_LOG_SYDNEY_A.md`. |
| B | 15 | **DONE (15/15)** | background agent | `analyst_targets_SYDNEY_B.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 13 TRADEABLE, 1 NOT_TRADEABLE (BVR.ASX), 2 NOFAQ (BRN, BVR). See `SESSION_LOG_SYDNEY_B.md`. |
| C | 25 | **DONE (25/25)** | background agent | `analyst_targets_SYDNEY_C.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 21 OK, 4 NOFAQ (CMW, CNU, CTD, CTT), all TRADEABLE. See `SESSION_LOG_SYDNEY_C.md`. |
| D | 9 | **DONE (9/9)** | background agent | `analyst_targets_SYDNEY_D.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 9 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_D.md`. |
| E | 6 | **DONE (6/6)** | background agent | `analyst_targets_SYDNEY_E.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 6 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_E.md`. |
| F | 4 | **DONE (4/4)** | background agent | `analyst_targets_SYDNEY_F.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 4 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_F.md`. |
| G | 5 | **DONE (5/5)** | background agent | `analyst_targets_SYDNEY_G.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 5 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_G.md`. |
| H | 6 | **DONE (6/6)** | background agent | `analyst_targets_SYDNEY_H.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 6 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_H.md`. |
| I | 11 | **DONE (11/11)** | background agent | `analyst_targets_SYDNEY_I.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 10 OK, 1 NOFAQ (IMU), all TRADEABLE. See `SESSION_LOG_SYDNEY_I.md`. |
| J | 3 | **DONE (3/3)** | background agent | `analyst_targets_SYDNEY_J.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 3 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_J.md`. |
| K | 3 | **DONE (3/3)** | background agent | `analyst_targets_SYDNEY_K.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 3 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_K.md`. |
| L | 6 | **DONE (6/6)** | background agent | `analyst_targets_SYDNEY_L.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 5 OK/TRADEABLE, 1 NOFAQ/NOT_TRADEABLE (LKE). See `SESSION_LOG_SYDNEY_L.md`. |
| M | 11 | **DONE (11/11)** | background agent | `analyst_targets_SYDNEY_M.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 10 OK, 1 NOFAQ (MMS), all TRADEABLE. See `SESSION_LOG_SYDNEY_M.md`. |
| N | 16 | **DONE (16/16)** | background agent | `analyst_targets_SYDNEY_N.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 14 OK, 2 NOFAQ (NSR, NVX); 1 NOT_TRADEABLE (NSR). See `SESSION_LOG_SYDNEY_N.md`. |
| O | 3 | **DONE (3/3)** | background agent | `analyst_targets_SYDNEY_O.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 3 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_O.md`. |
| P | 10 | **DONE (10/10)** | background agent | `analyst_targets_SYDNEY_P.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 10 OK/TRADEABLE. PWH.ASX has an unusual $1.00 analyst target vs 11.76 price — verified genuine tipranks data, not a scrape error. See `SESSION_LOG_SYDNEY_P.md`. |
| Q | 2 | **DONE (2/2)** | background agent | `analyst_targets_SYDNEY_Q.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. Both OK/TRADEABLE. See `SESSION_LOG_SYDNEY_Q.md`. |
| R | 11 | **DONE (11/11)** | background agent | `analyst_targets_SYDNEY_R.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 11 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_R.md`. |
| S | 21 | **DONE (21/21)** | background agent | `analyst_targets_SYDNEY_S.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 18 OK, 3 NOFAQ (SGR, SOL, SPK), all TRADEABLE. See `SESSION_LOG_SYDNEY_S.md`. |
| T | 9 | **DONE (9/9)** | background agent | `analyst_targets_SYDNEY_T.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 9 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_T.md`. |
| V | 5 | **DONE (5/5)** | background agent | `analyst_targets_SYDNEY_V.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. All 5 OK/TRADEABLE. See `SESSION_LOG_SYDNEY_V.md`. |
| W | 14 | **DONE (14/14)** | background agent | `analyst_targets_SYDNEY_W.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 12 OK, 2 NOFAQ (WBT, WJL); 1 NOT_TRADEABLE (WJL). See `SESSION_LOG_SYDNEY_W.md`. |
| X | 2 | **DONE (2/2)** | background agent | `analyst_targets_SYDNEY_X.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 1 OK, 1 NOFAQ (XYZ), both TRADEABLE. See `SESSION_LOG_SYDNEY_X.md`. |
| Y | 1 | **DONE (1/1)** | background agent | `analyst_targets_SYDNEY_Y.txt` | Complete 2026-08-28, zero blocks. Completeness audit passed. 1 OK/TRADEABLE. FINAL LETTER — SYDNEY EXCHANGE 100% COMPLETE (221/221). See `SESSION_LOG_SYDNEY_Y.md`. |

Total: 221 tickers across 24 letters (no U or Z tickers present).

## Procedure

1. Pick a letter marked `NOT STARTED`, claim it here (Status → `IN PROGRESS`), save before doing any real work.
2. Rigorously verify eToro login before starting (per `SYDNEY_PROJECT_LOG.md`).
3. Work the letter's tickers in sorted order (from `sydney_data.tsv`), per the v4 method + mandatory human-paced protocol.
4. Log progress in `SESSION_LOG_SYDNEY_<LETTER>.md`, update this board's row at each checkpoint.
5. On any block: stop immediately, checkpoint cleanly, report back — never solve/bypass.
6. Before declaring a letter done: run the completeness audit (diff against `sydney_data.tsv`).

## Merging (do only when the user asks)

Needs a `sydney`-specific merge script and site template — not yet built.
