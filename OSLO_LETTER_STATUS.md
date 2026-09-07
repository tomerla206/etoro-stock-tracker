# Oslo Letter Claim Board — v4 eToro Analysis-Tab Pass

**Read `OSLO_PROJECT_LOG.md` first.** Joins the back of the sequential queue (NYSE → Frankfurt → Paris → Sydney → Stockholm → Hong Kong → Oslo) — do not start until it's this project's turn and no other sibling agent is active.

## Ticker counts per letter (from `oslo_data.tsv`, built 2026-08-26, 232 tickers total, 0 duplicates)

| Letter | Ticker count | Status | Claimed by | Output file | Notes |
|---|---|---|---|---|---|
| 0-9 | 2 | **DONE** | background agent | `analyst_targets_OSLO_0-9.txt` | 2020.OL, 5PG.OL. Both NOFAQ, both TRADEABLE. Completeness audit clean. |
| A | 26 | **DONE** | background agent | `analyst_targets_OSLO_A.txt` | 26/26. Completeness audit clean (diff against oslo_data.tsv, both directions, zero gaps). AKRBP.OL, AKSO.OL, and AUTO.OL hit a widget-format variant (no LOW/AVG/HIGH summary box, computed manually from Top Analysts table) — see session log. |
| B | 14 | **DONE** | background agent | `analyst_targets_OSLO_B.txt` | 14/14. Completeness audit clean. BWLPG.OL hit the widget-format variant (2 Top Analysts, no summary box, computed manually). |
| C | 8 | **DONE** | background agent | `analyst_targets_OSLO_C.txt` | 8/8. Completeness audit clean. CAVEN.OL is NOT_TRADEABLE (both Trade buttons disabled). |
| D | 7 | **DONE** | background agent | `analyst_targets_OSLO_D.txt` | 7/7. Completeness audit clean. DNB.OL hit the widget-format variant. |
| E | 12 | **DONE** | background agent | `analyst_targets_OSLO_E.txt` | 12/12. Completeness audit clean. EQNR.OL hit the widget-format variant. |
| F | 2 | **DONE** | background agent | `analyst_targets_OSLO_F.txt` | 2/2. Completeness audit clean. FRO.OL hit the widget-format variant. |
| G | 7 | **DONE** | background agent | `analyst_targets_OSLO_G.txt` | 7/7. Completeness audit clean. GJF.OL hit the widget-format variant. |
| H | 12 | **DONE** | sequential agent 2026-08-29 | `analyst_targets_OSLO_H.txt` | 12/12. Completeness audit clean. HSHP.OL hit the widget-format variant (single analyst, no summary box, computed manually: 175.00/175.00/175.00). |
| I | 7 | **DONE** | sequential agent 2026-08-29 | `analyst_targets_OSLO_I.txt` | 7/7. Completeness audit clean. No widget-variant this letter. |
| J | 2 | **DONE** | sequential agent 2026-08-29 | `analyst_targets_OSLO_J.txt` | 2/2. Completeness audit clean. |
| K | 9 | **DONE** | sequential agent 2026-08-29 | `analyst_targets_OSLO_K.txt` | 9/9. Completeness audit clean. KOG.OL widget-variant (330.00/357.00/384.00). KMAR.OL is NOT_TRADEABLE. |
| L | 4 | **DONE** | sequential agent 2026-08-29 | `analyst_targets_OSLO_L.txt` | 4/4. Completeness audit clean. |
| M | 11 | **DONE** | sequential agent 2026-08-29 (aggressive pacing experiment) | `analyst_targets_OSLO_M.txt` | 11/11. All NOFAQ, all TRADEABLE. No widget-variant this letter. |
| N | 25 | **DONE** | sequential agent 2026-08-29 (aggressive pacing experiment) | `analyst_targets_OSLO_N.txt` | 25/25. Completeness audit clean. NEL.OL, NHY.OL, NOD.OL hit the widget-format variant (no LOW/AVG/HIGH summary box, computed manually from Top Analysts table). |
| O | 12 | **DONE** | sequential agent 2026-08-29 | `analyst_targets_OSLO_O.txt` | 12/12. Completeness audit clean. ODFB.OL hit the widget-format variant (single analyst, no summary box, computed manually: 130.00/130.00/130.00). ORK.OL (large-cap) genuinely NOFAQ, double-checked. Zero blocks. |
| P | 16 | **DONE** | sequential agent 2026-08-29 | `analyst_targets_OSLO_P.txt` | 16/16. Completeness audit clean. No widget-variant this letter. 3 NOT_TRADEABLE: PCIB.OL, PRYME.OL, PUBLI.OL. Zero blocks. |
| Q | 1 | **DONE** | sequential agent 2026-08-29 (Phase 1 pacing) | `analyst_targets_OSLO_Q.txt` | 1/1. Completeness audit clean. QEC.OL is NOFAQ. Zero blocks. |
| R | 5 | **DONE** | sequential agent 2026-08-29 (Phase 1 pacing) | `analyst_targets_OSLO_R.txt` | 5/5. Completeness audit clean. All NOFAQ, all TRADEABLE. Zero blocks. |
| S | 25 | **DONE** | sequential agent 2026-08-29 (Phase 1 pacing) | `analyst_targets_OSLO_S.txt` | 25/25. Completeness audit clean. STB.OL and SUBC.OL hit the widget-format variant (computed manually: STB 150/177/216, SUBC 367/389/415). All TRADEABLE. Zero blocks. |
| T | 7 | **DONE** | sequential agent 2026-08-29 (Phase 1 pacing) | `analyst_targets_OSLO_T.txt` | 7/7. Completeness audit clean. TEL.OL and TGS.OL hit widget-variant (TEL 135/147.50/160, TGS 60/146.67/200). TIETO.OL is NOT_TRADEABLE. Zero blocks. **Phase 1 (Q,R,S,T=38 tickers) complete, zero blocks.** |
| V | 8 | **DONE** | sequential agent 2026-08-29 (Phase 2 pacing) | `analyst_targets_OSLO_V.txt` | 8/8. Completeness audit clean. VAR.OL hit widget-variant (50/53/55). All TRADEABLE. Zero blocks. |
| W | 5 | **DONE** | sequential agent 2026-08-29 (Phase 2 pacing) | `analyst_targets_OSLO_W.txt` | 5/5. Completeness audit clean. All NOFAQ, all TRADEABLE. Zero blocks. |
| X | 1 | **DONE** | sequential agent 2026-08-29 (Phase 2 pacing) | `analyst_targets_OSLO_X.txt` | 1/1. Completeness audit clean. XPLRA.OL NOFAQ, TRADEABLE. Zero blocks. |
| Y | 1 | **DONE** | sequential agent 2026-08-29 (Phase 2 pacing) | `analyst_targets_OSLO_Y.txt` | 1/1. Completeness audit clean. YAR.OL (large-cap) double-checked genuinely NOFAQ, TRADEABLE. Zero blocks. |
| Z | 3 | **DONE** | sequential agent 2026-08-29 (Phase 2 pacing) | `analyst_targets_OSLO_Z.txt` | 3/3. Completeness audit clean. All NOFAQ, all TRADEABLE. Zero blocks. **Oslo project fully complete — all 26 letter groups DONE, 232/232 tickers.** |

Total: 232 tickers across 26 groups (no U tickers present).

## Procedure

1. Confirm it's this project's turn in the sequential queue and no other sibling-project agent is active.
2. Pick a letter marked `NOT STARTED`, claim it here (Status → `IN PROGRESS`), save before doing any real work.
3. Rigorously verify eToro login before starting (per `OSLO_PROJECT_LOG.md`).
4. Work the letter's tickers in sorted order (from `oslo_data.tsv`), per the v4 method + mandatory human-paced protocol.
5. Log progress in `SESSION_LOG_OSLO_<LETTER>.md`, update this board's row at each checkpoint.
6. On any block: stop immediately, checkpoint cleanly, report back — never solve/bypass.
7. Before declaring a letter done: run the completeness audit (diff against `oslo_data.tsv`).

## Merging (do only when the user asks)

Extend `generate_exchange_rows.py`'s `EXCHANGES` list with `("oslo_data.tsv", "Oslo")`, regenerate, append to `all_rows.html`, re-run `merge_analyst_targets.py`, reassemble, republish — same process as the other exchanges.
