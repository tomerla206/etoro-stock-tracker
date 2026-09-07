# Tokyo Group Claim Board — v4 eToro Analysis-Tab Pass

## ✅ TOKYO PROJECT FULLY DONE (2026-08-29) — 226/226, zero gaps/duplicates

All 6 groups (TY1-TY6) complete. Full cross-check of all 6 `analyst_targets_TOKYO_TY*.txt` files against `tokyo_data.tsv` confirmed exact match, 226/226 tickers, no gaps, no duplicates. Session completed TY3's remaining 24 tickers (resumed cleanly at 5801.T after router power-cycle, login re-verified rigorously) plus all of TY4 (38), TY5 (38), TY6 (36) — 136 tickers total this session, zero blocks encountered despite far exceeding the ~30-33 ticker range where prior sessions hit ordinary lockouts. This is further evidence for the per-session cooldown/quota theory over the pacing theory, though it's also possible the block risk is simply variable. Tokyo is the last exchange in the original sequential queue before the 13-exchange batch (`EXTRA_EXCHANGES_LOG.md`).

**Read `TOKYO_PROJECT_LOG.md` first.** Joins the back of the sequential queue (NYSE → Frankfurt → Paris → Sydney → Stockholm → Hong Kong → Oslo → Tokyo) — do not start until it's this project's turn and no other sibling agent is active.

## Ticker groups (from `tokyo_data.tsv`, built 2026-08-26, 226 tickers total, 0 duplicates)

All tickers are numeric (or numeric+letter) `.T` codes — no natural alphabetic grouping, so split into 6 sequential chunks of ~38 tickers each in sorted-tsv order.

| Group | Ticker count | Status | Claimed by | Output file | Range |
|---|---|---|---|---|---|
| TY1 | 38 | DONE (38/38, completeness audit clean) | this session | `analyst_targets_TOKYO_TY1.txt` | 1332.T-3861.T |
| TY2 | 38 | DONE (38/38, completeness audit clean) | this session | `analyst_targets_TOKYO_TY2.txt` | 4004.T-5201.T |
| TY3 | 38 | DONE (38/38, completeness audit clean) | this session | `analyst_targets_TOKYO_TY3.txt` | 5214.T-6506.T |
| TY4 | 38 | DONE (38/38, completeness audit clean) | this session | `analyst_targets_TOKYO_TY4.txt` | 6526.T-7270.T |
| TY5 | 38 | DONE (38/38, completeness audit clean) | this session | `analyst_targets_TOKYO_TY5.txt` | 7272.T-8725.T |
| TY6 | 36 | DONE (36/36, completeness audit clean) | this session | `analyst_targets_TOKYO_TY6.txt` | 8750.T-9984.T |

Total: 226 tickers across 6 groups.

## Procedure

1. Confirm it's this project's turn in the sequential queue and no other sibling-project agent is active.
2. Pick a group marked `NOT STARTED`, claim it here (Status → `IN PROGRESS`), save before doing any real work.
3. Rigorously verify eToro login before starting (per `TOKYO_PROJECT_LOG.md`).
4. Work the group's tickers in `tokyo_data.tsv` order, per the v4 method + mandatory human-paced protocol.
5. Log progress in `SESSION_LOG_TOKYO_<GROUP>.md`, update this board's row at each checkpoint.
6. On any block: stop immediately, checkpoint cleanly, report back — never solve/bypass.
7. Before declaring a group done: run the completeness audit (diff against `tokyo_data.tsv`).

## Merging (do only when the user asks)

Extend `generate_exchange_rows.py`'s `EXCHANGES` list with `("tokyo_data.tsv", "Tokyo")`, regenerate, append to `all_rows.html`, re-run `merge_analyst_targets.py`, reassemble, republish — same process as the other exchanges.
