# Milan Letter Claim Board — v4 eToro Analysis-Tab Pass

**Read `MILAN_PROJECT_LOG.md` first.** Joins the back of the sequential queue (NYSE → Frankfurt → Paris → Sydney → Stockholm → Hong Kong → Oslo → Tokyo → Milan) — do not start until it's this project's turn and no other sibling agent is active.

## Ticker counts per letter (from `milan_data.tsv`, built 2026-08-26, 78 tickers total, 0 duplicates)

| Letter | Ticker count | Status | Claimed by | Output file | Notes |
|---|---|---|---|---|---|
| A | 8 | DONE | this session | `analyst_targets_MILAN_A.txt` | 8/8, all TRADEABLE, no blocks |
| B | 9 | DONE | this session | `analyst_targets_MILAN_B.txt` | 9/9, all TRADEABLE, no blocks |
| C | 4 | DONE | this session | `analyst_targets_MILAN_C.txt` | 4/4, all TRADEABLE, no blocks |
| D | 4 | DONE | this session | `analyst_targets_MILAN_D.txt` | 4/4, all TRADEABLE, no blocks |
| E | 4 | DONE | this session | `analyst_targets_MILAN_E.txt` | 4/4, all TRADEABLE, no blocks |
| F | 2 | DONE | this session | `analyst_targets_MILAN_F.txt` | 2/2, all TRADEABLE, no blocks |
| G | 2 | DONE | this session | `analyst_targets_MILAN_G.txt` | 2/2, all TRADEABLE, no blocks |
| H | 1 | DONE | this session | `analyst_targets_MILAN_H.txt` | 1/1, TRADEABLE, no blocks |
| I | 9 | DONE | this session | `analyst_targets_MILAN_I.txt` | 9/9, all TRADEABLE, no blocks |
| J | 1 | DONE | this session | `analyst_targets_MILAN_J.txt` | 1/1, TRADEABLE, no blocks |
| L | 2 | DONE | this session | `analyst_targets_MILAN_L.txt` | 2/2, all TRADEABLE, no blocks |
| M | 5 | DONE | this session | `analyst_targets_MILAN_M.txt` | 5/5, all TRADEABLE, no blocks |
| N | 1 | DONE | this session | `analyst_targets_MILAN_N.txt` | 1/1, TRADEABLE, no blocks |
| P | 4 | DONE | this session | `analyst_targets_MILAN_P.txt` | 4/4, all TRADEABLE, no blocks |
| R | 4 | DONE | this session | `analyst_targets_MILAN_R.txt` | 4/4, all TRADEABLE, no blocks |
| S | 8 | DONE | this session | `analyst_targets_MILAN_S.txt` | 8/8, all TRADEABLE, no blocks |
| T | 6 | DONE | this session | `analyst_targets_MILAN_T.txt` | 6/6, all TRADEABLE, no blocks |
| U | 2 | DONE | this session | `analyst_targets_MILAN_U.txt` | 2/2, all TRADEABLE, no blocks |
| W | 1 | DONE | this session | `analyst_targets_MILAN_W.txt` | 1/1, TRADEABLE, no blocks |
| Z | 1 | DONE | this session | `analyst_targets_MILAN_Z.txt` | 1/1, TRADEABLE, no blocks |

Total: 78 tickers across 20 letters. Smallest exchange in this project family — could plausibly be done in one session.

## Procedure

1. Confirm it's this project's turn in the sequential queue and no other sibling-project agent is active.
2. Pick a letter marked `NOT STARTED`, claim it here (Status → `IN PROGRESS`), save before doing any real work.
3. Rigorously verify eToro login before starting (per `MILAN_PROJECT_LOG.md`).
4. Work the letter's tickers in sorted order (from `milan_data.tsv`), per the v4 method + mandatory human-paced protocol.
5. Log progress in `SESSION_LOG_MILAN_<LETTER>.md`, update this board's row at each checkpoint.
6. On any block: stop immediately, checkpoint cleanly, report back — never solve/bypass.
7. Before declaring a letter done: run the completeness audit (diff against `milan_data.tsv`).

## Merging (do only when the user asks)

Extend `generate_exchange_rows.py`'s `EXCHANGES` list with `("milan_data.tsv", "Milan")`, regenerate, append to `all_rows.html`, re-run `merge_analyst_targets.py`, reassemble, republish — same process as the other exchanges.
