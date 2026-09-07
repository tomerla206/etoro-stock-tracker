# Hong Kong Group Claim Board — v4 eToro Analysis-Tab Pass

**Read `HONGKONG_PROJECT_LOG.md` first.** Joins the back of the sequential queue (NYSE → Frankfurt → Paris → Sydney → Stockholm → Hong Kong) — do not start until it's this project's turn and no other sibling agent is active.

## Ticker groups (from `hongkong_data.tsv`, built 2026-08-26, 232 tickers total, 0 duplicates)

All tickers are numeric `.HK` codes — no natural alphabetic grouping, so split into 6 sequential chunks of ~39 tickers each in sorted-tsv order.

| Group | Ticker count | Status | Claimed by | Output file | Range |
|---|---|---|---|---|---|
| HK1 | 39 | **DONE** | active agent | `analyst_targets_HONGKONG_HK1.txt` | 00001.HK-02386.HK. Completeness audit passed (39/39, 0 gaps, 0 dupes). 39 NOFAQ (100%), 38 TRADEABLE, 1 NOT_TRADEABLE (00981.HK SMIC). See note below on systemic NOFAQ finding. |
| HK2 | 39 | **DONE** | active agent | `analyst_targets_HONGKONG_HK2.txt` | 02388.HK-1157.HK. Completeness audit passed (39/39, 0 gaps, 0 dupes). 14 NOFAQ, 25 OK, 34 TRADEABLE, 5 NOT_TRADEABLE (03333 Evergrande delisting, 0728/0762/0883/0941 sanctioned China entities). |
| HK3 | 39 | **DONE** | active agent | `analyst_targets_HONGKONG_HK3.txt` | 1171.HK-1833.HK. Completeness audit passed (39/39, 0 gaps, 0 dupes). 15 NOFAQ, 24 OK, 37 TRADEABLE, 2 NOT_TRADEABLE (1186 China Railway Construction, 1800 China Communications Construction — both sanctioned entities). |
| HK4 | 39 | **DONE** | active agent | `analyst_targets_HONGKONG_HK4.txt` | 1873.HK-2799.HK. Completeness audit passed (39/39, 0 gaps, 0 dupes). 8 NOFAQ, 31 OK, 39 TRADEABLE, 0 NOT_TRADEABLE. |
| HK5 | 39 | **DONE** | active agent | `analyst_targets_HONGKONG_HK5.txt` | 288.HK-6186.HK. Block cleared after user power-cycled router; 3808.HK redone fresh, rest completed with conservative pacing, no further blocks. Completeness audit passed (39/39, 0 gaps, 0 dupes). 16 NOFAQ, 23 OK, 39 TRADEABLE, 0 NOT_TRADEABLE. |
| HK6 | 37 | **DONE** | active agent | `analyst_targets_HONGKONG_HK6.txt` | 6198.HK-9999.HK. Completeness audit passed (37/37, 0 gaps, 0 dupes). 16 NOFAQ, 21 OK, 35 TRADEABLE, 2 NOT_TRADEABLE (7489.HK VOYAH Automobile Technology — trade buttons disabled=true, anomalous price data suggesting recent/problematic listing; 9658.HK Super Hi International — trade buttons disabled=true, Market Cap/Volume/PE/Revenue all "-"). |

## ALL OF HONG KONG COMPLETE — 232/232 tickers across HK1-HK6, all groups DONE.

Total: 232 tickers across 6 groups.

## Procedure

1. Confirm it's this project's turn in the sequential queue and no other sibling-project agent is active.
2. Pick a group marked `NOT STARTED`, claim it here (Status → `IN PROGRESS`), save before doing any real work.
3. Rigorously verify eToro login before starting (per `HONGKONG_PROJECT_LOG.md`).
4. Work the group's tickers in `hongkong_data.tsv` order, per the v4 method + mandatory human-paced protocol.
5. Log progress in `SESSION_LOG_HONGKONG_<GROUP>.md`, update this board's row at each checkpoint.
6. On any block: stop immediately, checkpoint cleanly, report back — never solve/bypass.
7. Before declaring a group done: run the completeness audit (diff against `hongkong_data.tsv`).

## Merging (do only when the user asks)

Extend `generate_exchange_rows.py`'s `EXCHANGES` list with `("hongkong_data.tsv", "Hong Kong")`, regenerate, append to `all_rows.html`, re-run `merge_analyst_targets.py`, reassemble, republish — same process as the other five exchanges.
