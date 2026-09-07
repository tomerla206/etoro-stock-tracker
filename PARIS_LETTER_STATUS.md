# Paris Letter Claim Board — v4 Combined eToro Analysis-Tab Pass

## ✅ PARIS EXCHANGE FULLY COMPLETE (2026-08-28) — all 416/416 tickers, all 27 groups DONE

Full-project completeness audit passed: concatenated all 27 `analyst_targets_PARIS_*.txt` files, diffed against `paris_data.tsv`'s full 416-ticker list — 0 gaps, 0 duplicates, exact match both directions. Paris moves to fully done; per the project queue, Sydney is next up.

Along the way, a pre-existing data bug was found and fixed in 7 of the 27 group files (J, K, L, M, N, O, P): each had a stray leading `<line-number><TAB>` prefix baked into the ticker column from an earlier session (e.g. `1\tPAR.PA\t...` instead of `PAR.PA\t...`). This didn't corrupt any actual analyst/price data — only the leading column — but would have broken ticker-column matching in the completeness audit and any downstream merge script. All 7 files were rewritten with the stray prefix stripped; verified byte-identical otherwise.

**Read `PARIS_PROJECT_LOG.md` first.** Ran in parallel with NYSE and Frankfurt by explicit user decision 2026-08-26 (policy since reverted to sequential, see `PROJECT_LOG.md`'s v4 method section).

## Ticker counts per group (from `paris_data.tsv`, built 2026-08-26, 416 tickers total, 0 duplicates)

| Group | Ticker count | Status | Claimed by | Output file | Notes |
|---|---|---|---|---|---|
| 7 | 1 | **DONE** | | `analyst_targets_PARIS_7.txt` | 74SW.PA (74Software SA). 1/1 complete. OK/TRADEABLE, Low 47.00/Avg 51.00/High 55.00. 0 blocks. |
| A1 | 62 | **DONE** | | `analyst_targets_PARIS_A1.txt` | AB.PA-ALESE.PA. 62/62 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks in final session (one transient tab stall on ALCOF.PA, resolved). See `SESSION_LOG_PARIS_A1.md`. |
| A2 | 62 | **DONE** | | `analyst_targets_PARIS_A2.txt` | ALFER.PA-ALODC.PA. 62/62 complete, completeness audit passed (0 gaps, 0 duplicates). 0 blocks. 3 legitimate NOT_TRADEABLE (ALHG, ALMCP, ALNEV). See `SESSION_LOG_PARIS_A2.md`. |
| A3 | 61 | **DONE** | | `analyst_targets_PARIS_A3.txt` | ALOKW.PA-AYV.PA. 61/61 complete, completeness audit passed (0 gaps, 0 duplicates). 0 blocks. 1 legitimate NOT_TRADEABLE (ALTD). See `SESSION_LOG_PARIS_A3.md`. |
| B | 15 | **DONE** | | `analyst_targets_PARIS_B.txt` | BAIN.PA-BVI.PA. 15/15 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks. 5 OK (BEN, BIM, BN, BNP, BVI), 10 NOFAQ. All 15 TRADEABLE. See `SESSION_LOG_PARIS_B.md`. |
| C | 30 | **DONE** | | `analyst_targets_PARIS_C.txt` | CA.PA-CVX.PA. 30/30 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks. 6 OK (CA, CAP, COFA, COTY, COV, CS), 24 NOFAQ. All 30 TRADEABLE. See `SESSION_LOG_PARIS_C.md`. |
| D | 8 | **DONE** | | `analyst_targets_PARIS_D.txt` | DBG.PA-DSY.PA. 8/8 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks. 4 OK (DEC, DG, DIM, DSY), 4 NOFAQ. All 8 TRADEABLE. See `SESSION_LOG_PARIS_D.md`. |
| E | 21 | **DONE** | | `analyst_targets_PARIS_E.txt` | EAPI.PA-EXPL.PA. 21/21 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks. 11 OK, 10 NOFAQ. All 21 TRADEABLE. See `SESSION_LOG_PARIS_E.md`. |
| F | 8 | **DONE** | | `analyst_targets_PARIS_F.txt` | FDE.PA-FRVIA.PA. 8/8 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks. 4 OK (FDJU, FGR, FR, FRVIA), 4 NOFAQ. All 8 TRADEABLE. See `SESSION_LOG_PARIS_F.md`. |
| G | 13 | **DONE** | | `analyst_targets_PARIS_G.txt` | GAM.PA-GUI.PA. 13/13 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks. 4 OK (GET, GFC, GLE, GTT), 9 NOFAQ. All 13 TRADEABLE. See `SESSION_LOG_PARIS_G.md`. |
| H | 3 | **DONE** | | `analyst_targets_PARIS_H.txt` | HCO.PA-HO.PA. 3/3 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks. 1 OK (HO), 2 NOFAQ. All 3 TRADEABLE. See `SESSION_LOG_PARIS_H.md`. |
| I | 12 | **DONE** | | `analyst_targets_PARIS_I.txt` | IAM.PA-IVA.PA. 12/12 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). 0 blocks. 5 OK (ICAD, IDL, IPN, IVA), 7 NOFAQ. All 12 TRADEABLE. See `SESSION_LOG_PARIS_I.md`. |
| J | 2 | **DONE** | | `analyst_targets_PARIS_J.txt` | JBOG.PA-JCQ.PA. 2/2 complete, completeness audit passed (0 gaps, 0 duplicates). 0 blocks. Both NOFAQ, both TRADEABLE. [2026-08-28: fixed a stray leading line-number+tab bug found in the raw file, same class of bug as group P — data values unaffected, only cosmetic prefix stripped.] See `SESSION_LOG_PARIS_J.md`. |
| K | 2 | **DONE** | | `analyst_targets_PARIS_K.txt` | KER.PA-KOF.PA. 2/2 complete, completeness audit passed (0 gaps, 0 duplicates). 0 blocks. 1 OK (KER), 1 NOFAQ. Both TRADEABLE. [2026-08-28: fixed stray leading line-number+tab bug, same as group J/P.] See `SESSION_LOG_PARIS_K.md`. |
| L | 11 | **DONE** | | `analyst_targets_PARIS_L.txt` | LACR.PA-LTA.PA. 11/11 complete, completeness audit passed (0 gaps, 0 duplicates). 0 blocks. 2 OK (LI, LR), 9 NOFAQ. 1 NOT_TRADEABLE (LTA). [2026-08-28: fixed stray leading line-number+tab bug, same as group J/K/P.] See `SESSION_LOG_PARIS_L.md`. |
| M | 14 | **DONE** | | `analyst_targets_PARIS_M.txt` | MAAT.PA-MTU.PA. 14/14 complete, completeness audit passed (0 gaps, 0 duplicates). 0 blocks. 6 OK, 8 NOFAQ. All 14 TRADEABLE. [2026-08-28: fixed stray leading line-number+tab bug, same as group J/K/L/P.] See `SESSION_LOG_PARIS_M.md`. |
| N | 9 | **DONE** | | `analyst_targets_PARIS_N.txt` | NACON.PA-NXI.PA. 9/9 complete, completeness audit passed (0 gaps, 0 duplicates). 0 blocks. 2 OK, 7 NOFAQ. 1 NOT_TRADEABLE (NOKIA). [2026-08-28: fixed stray leading line-number+tab bug, same as group J/K/L/M/P.] See `SESSION_LOG_PARIS_N.md`. |
| O | 5 | **DONE** | | `analyst_targets_PARIS_O.txt` | ODET.PA-OSE.PA. 5/5 complete, completeness audit passed (0 gaps, 0 duplicates). 0 blocks. 3 OK, 2 NOFAQ. All 5 TRADEABLE. [2026-08-28: fixed stray leading line-number+tab bug, same as group J/K/L/M/N/P.] See `SESSION_LOG_PARIS_O.md`. |
| P | 13 | **DONE** | | `analyst_targets_PARIS_P.txt` | PAR.PA-PUB.PA. 13/13 complete, completeness audit passed (0 gaps, 0 duplicates vs paris_data.tsv). Also fixed a pre-existing data bug found on resume: first 7 lines had stray leading line-number+tab baked into file content from an earlier session — stripped clean. PLNW.PA redone fresh (TipRanks 26.00/26.00/26.00 reconfirmed, eToro side newly captured). 3 OK (PLNW, PLX, PUB), 10 NOFAQ. All 13 TRADEABLE. 0 blocks this session (login re-verified fresh via AAPL ungated-panel check before starting). See `SESSION_LOG_PARIS_P.md`. |
| Q | 1 | **DONE** | | `analyst_targets_PARIS_Q.txt` | QDT.PA. 1/1 complete, completeness audit passed. 0 blocks. NOFAQ, TRADEABLE. See `SESSION_LOG_PARIS_Q.md`. |
| R | 9 | **DONE** | | `analyst_targets_PARIS_R.txt` | RBO.PA-RXL.PA. 9/9 complete, completeness audit passed. 0 blocks. 5 OK, 4 NOFAQ. All 9 TRADEABLE. See `SESSION_LOG_PARIS_R.md`. |
| S | 24 | **DONE** | | `analyst_targets_PARIS_S.txt` | S30.PA-SWP.PA. 24/24 complete, completeness audit passed. 0 blocks. 12 OK, 12 NOFAQ. All 24 TRADEABLE. See `SESSION_LOG_PARIS_S.md`. |
| T | 9 | **DONE** | | `analyst_targets_PARIS_T.txt` | TE.PA-TTE.PA. 9/9 complete, completeness audit passed. 0 blocks. 7 OK, 2 NOFAQ. All 9 TRADEABLE. See `SESSION_LOG_PARIS_T.md`. |
| U | 2 | **DONE** | | `analyst_targets_PARIS_U.txt` | UBI.PA, URW.PA. 2/2 complete, completeness audit passed. 0 blocks. 2 OK. Both TRADEABLE. See `SESSION_LOG_PARIS_U.md`. |
| V | 15 | **DONE** | | `analyst_targets_PARIS_V.txt` | VAC.PA-VU.PA. 15/15 complete, completeness audit passed. 0 blocks. 9 OK, 6 NOFAQ. All 15 TRADEABLE. See `SESSION_LOG_PARIS_V.md`. |
| W | 3 | **DONE** | | `analyst_targets_PARIS_W.txt` | WAGA.PA, WAVE.PA, WLN.PA. 3/3 complete, completeness audit passed. 0 blocks. 1 OK, 2 NOFAQ. All 3 TRADEABLE. See `SESSION_LOG_PARIS_W.md`. |
| X | 1 | **DONE** | | `analyst_targets_PARIS_X.txt` | XFAB.PA. 1/1 complete. 0 blocks. OK, TRADEABLE. Low 6.00/Avg 8.25/High 10.50. |

Total: 416 tickers across 27 groups (A split into A1/A2/A3).

## Procedure

1. Pick a group marked `NOT STARTED`, claim it here (Status → `IN PROGRESS`), save before doing any real work.
2. Rigorously verify eToro login before starting (per `PARIS_PROJECT_LOG.md`).
3. Work the group's tickers in sorted order (from `paris_data.tsv`), per the v4 method + mandatory human-paced protocol.
4. Log progress in `SESSION_LOG_PARIS_<GROUP>.md`, update this board's row at each checkpoint.
5. On any block: stop immediately, checkpoint cleanly, report back — never solve/bypass.
6. Before declaring a group done: run the completeness audit (diff against `paris_data.tsv`).

## Merging (do only when the user asks)

Needs a `paris`-specific merge script and site template — not yet built.
