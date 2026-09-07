# Frankfurt Letter Claim Board — v4 Combined eToro Analysis-Tab Pass

**Read `FRANKFURT_PROJECT_LOG.md` first.** Runs in parallel with the NYSE project by explicit user decision 2026-08-26 (see that file's policy note) — normally this project would follow the same "one active agent across all exchanges" rule as NASDAQ/NYSE, but that's been relaxed here specifically.

## Ticker counts per group (from `frankfurt_data.tsv`, built 2026-08-26, 436 tickers total, 0 duplicates)

| Group | Ticker count | Status | Claimed by | Output file | Notes |
|---|---|---|---|---|---|
| 0-9 | 14 | **DONE** | background agent | `analyst_targets_FRANKFURT_0-9.txt` | 14/14 complete, audit passed. 6 OK / 8 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| A | 39 | **DONE** | background agent | `analyst_targets_FRANKFURT_A.txt` | 2026-08-28: resumed with fresh login (strict sequential mode, sole active agent), redid AMI.DE clean (block had cleared), completed remaining 10 tickers (AMI.DE, AMM.DE, AMV0.DE, AMZN.EUR, AOF.DE, APM.DE, AT1.DE, AUS.DE, AVGO.EUR, AZ2.DE) with zero blocks. 39/39, completeness audit passed (0 gaps, 0 extras vs frankfurt_data.tsv). |
| B | 25 | **DONE** | background agent | `analyst_targets_FRANKFURT_B.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 25/25, completeness audit passed (0 gaps, 0 extras). |
| C | 22 | **DONE** | background agent | `analyst_targets_FRANKFURT_C.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 22/22, completeness audit passed (0 gaps, 0 extras). |
| D | 29 | **DONE** | background agent | `analyst_targets_FRANKFURT_D.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 29/29, completeness audit passed (0 gaps, 0 extras). 14 OK / 15 NOFAQ / 1 NOT_TRADEABLE (DFV.DE, real eToro slug dfv0.de) / 0 CVR. |
| E | 23 | **DONE** | background agent | `analyst_targets_FRANKFURT_E.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 23/23, completeness audit passed (0 gaps, 0 extras). 9 OK / 14 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| F | 14 | **DONE** | background agent | `analyst_targets_FRANKFURT_F.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 14/14, completeness audit passed (0 gaps, 0 extras). 8 OK / 6 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| G | 13 | **DONE** | background agent | `analyst_targets_FRANKFURT_G.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 13/13, completeness audit passed (0 gaps, 0 extras). 7 OK / 6 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| H | 25 | **DONE** | background agent | `analyst_targets_FRANKFURT_H.txt` | 2026-08-28: resumed with fresh login (strict sequential mode), redid HBH.DE clean (block had cleared, data matched pre-block read exactly), completed remaining 19 tickers with zero blocks. 25/25, completeness audit passed (0 gaps, 0 extras). 11 OK / 14 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| I | 14 | **DONE** | background agent | `analyst_targets_FRANKFURT_I.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 14/14, completeness audit passed (0 gaps, 0 extras). 6 OK / 8 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| J | 5 | **DONE** | background agent | `analyst_targets_FRANKFURT_J.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 5/5, completeness audit passed (0 gaps, 0 extras). 3 OK / 2 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| K | 12 | **DONE** | background agent | `analyst_targets_FRANKFURT_K.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 12/12, completeness audit passed (0 gaps, 0 extras). 7 OK / 5 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| L | 11 | **DONE** | background agent | `analyst_targets_FRANKFURT_L.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 11/11, completeness audit passed (0 gaps, 0 extras). 6 OK / 5 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| M | 32 | **DONE** | background agent | `analyst_targets_FRANKFURT_M.txt` | 2026-08-28: completed in strict sequential mode, zero blocks (one transient Chrome-extension disconnect, recovered immediately). 32/32, completeness audit passed (0 gaps, 0 extras). 11 OK / 20 NOFAQ / 1 NOT_TRADEABLE (MDG1.DE) / 0 CVR. |
| N | 16 | **DONE** | background agent | `analyst_targets_FRANKFURT_N.txt` | 2026-08-28: completed in strict sequential mode, zero blocks (one transient tab hang, recovered with fresh tab). 16/16, completeness audit passed (0 gaps, 0 extras). 6 OK / 10 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| O | 5 | **DONE** | background agent | `analyst_targets_FRANKFURT_O.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 5/5, completeness audit passed (0 gaps, 0 extras). 2 OK / 3 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| P | 18 | **DONE** | background agent | `analyst_targets_FRANKFURT_P.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 18/18, completeness audit passed (0 gaps, 0 extras). 9 OK / 9 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| Q | 3 | **DONE** | background agent | `analyst_targets_FRANKFURT_Q.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 3/3, completeness audit passed (0 gaps, 0 extras). 1 OK / 2 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| R | 12 | **DONE** | background agent | `analyst_targets_FRANKFURT_R.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 12/12, completeness audit passed (0 gaps, 0 extras). 8 OK / 4 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| S | 41 | **DONE** | background agent | `analyst_targets_FRANKFURT_S.txt` | 2026-08-28: completed in strict sequential mode. Prior process was interrupted at 40/41 (app restart, not a block); resumed same session, fetched SZU.DE (Suedzucker, price 12.640, Low 9.00/Avg 11.35/High 13.70, OK, TRADEABLE) cleanly with fresh login. 41/41, completeness audit passed (0 gaps, 0 extras). 19 OK / 22 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| T | 20 | **DONE** | background agent | `analyst_targets_FRANKFURT_T.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 20/20, completeness audit passed (0 gaps, 0 extras). 11 OK / 9 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| U | 7 | **DONE** | background agent | `analyst_targets_FRANKFURT_U.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 7/7, completeness audit passed (0 gaps, 0 extras). 2 OK / 5 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| V | 19 | **DONE** | background agent | `analyst_targets_FRANKFURT_V.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 19/19, completeness audit passed (0 gaps, 0 extras). 8 OK / 11 NOFAQ / 1 NOT_TRADEABLE (VROS.DE) / 0 CVR. |
| W | 11 | **DONE** | background agent | `analyst_targets_FRANKFURT_W.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 11/11, completeness audit passed (0 gaps, 0 extras). 5 OK / 5 NOFAQ / 1 NOT_TRADEABLE (WDI.DE, Wirecard) / 0 CVR. |
| X | 2 | **DONE** | background agent | `analyst_targets_FRANKFURT_X.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 2/2, completeness audit passed (0 gaps, 0 extras). 0 OK / 2 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| Y | 2 | **DONE** | background agent | `analyst_targets_FRANKFURT_Y.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 2/2, completeness audit passed (0 gaps, 0 extras). 1 OK / 1 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. |
| Z | 2 | **DONE** | background agent | `analyst_targets_FRANKFURT_Z.txt` | 2026-08-28: completed in strict sequential mode, zero blocks. 2/2, completeness audit passed (0 gaps, 0 extras). 1 OK / 1 NOFAQ / 0 NOT_TRADEABLE / 0 CVR. **This is the final letter — ALL OF FRANKFURT (436 tickers, 27 groups) IS NOW COMPLETE.** |

Total: 436 tickers across 27 groups (26 letters + 0-9 bucket).

## PROJECT COMPLETE — 2026-08-28

**All 27 groups DONE. Project-wide completeness audit passed: 436/436 tickers present across all `analyst_targets_FRANKFURT_*.txt` files, 0 gaps vs `frankfurt_data.tsv`, 0 extras, 0 duplicates.** The Frankfurt exchange scraping project is finished. Per `FRANKFURT_PROJECT_LOG.md`, merging into a standalone site is deferred until the user asks for it.

## Procedure

1. Pick a group marked `NOT STARTED`, claim it here (Status → `IN PROGRESS`), save before doing any real work.
2. Rigorously verify eToro login before starting (per `FRANKFURT_PROJECT_LOG.md`).
3. Work the group's tickers in sorted order (from `frankfurt_data.tsv`), per the v4 method + mandatory human-paced protocol.
4. Log progress in `SESSION_LOG_FRANKFURT_<GROUP>.md`, update this board's row at each checkpoint.
5. On any block: stop immediately, checkpoint cleanly, report back — never solve/bypass.
6. Before declaring a group done: run the completeness audit (diff against `frankfurt_data.tsv`).

## Merging (do only when the user asks)

Needs a `frankfurt`-specific merge script and site template — not yet built (build when first requested).
