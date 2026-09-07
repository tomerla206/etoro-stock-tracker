# Session Log — Paris Group P (DONE)

Resumed in a fresh session. Login re-verified fresh at session start via AAPL check:
navigated to `https://www.etoro.com/markets/aapl/research`, confirmed real-time "Prices by NASDAQ, in USD"
(Off-hours), logged in as "Tomer Lalo Schwartz", AND took a screenshot confirming the Research/Analysis panel
was fully ungated (Low 245.00 / Avg 337.09 / High 400.00, 24 ranked analysts, ratings table visible) —
not just the price label, per the lesson from the two prior blocks on this letter.

## Completed this session

1. **PLNW.PA redone completely fresh** (both sides, as instructed):
   - TipRanks: Low 26.00 / Avg 26.00 / High 26.00, 1 analyst (UBS, Hold, 18.08.26) — reconfirmed exactly matches the stale value from the prior blocked session.
   - eToro research: "Prices by Euronext, in EUR" (real-time, Market Open), price 24.650, 2 Trade buttons both `disabled:false` → TRADEABLE.
   - Recorded: OK/TRADEABLE.

2. **PLX.PA** — TipRanks Low/Avg/High 11.90/11.90/11.90 (1 analyst, consensus Hold). eToro: 16.230, real-time, TRADEABLE. OK.

3. **POMRY.PA** — TipRanks: "This stock has no research data" → NOFAQ. eToro: 10.05, real-time, TRADEABLE.

4. **POXEL.PA** — NOFAQ. eToro: 0.2020, Market Closed but still real-time-labeled ("Prices by Euronext", not "Delayed"), TRADEABLE.

5. **PRC.PA** — NOFAQ. eToro: 3.860, real-time, TRADEABLE.

6. **PUB.PA** — TipRanks Low/Avg/High 110.00/120.67/133.00 (3 analysts, Strong Buy). eToro: 101.20, real-time, TRADEABLE. OK.

No blocks this session — all 6 remaining tickers went cleanly with the standard 3-8s per-ticker pacing.

## Data-integrity fix found on resume

The output file `analyst_targets_PARIS_P.txt` had a pre-existing bug from an earlier session: the first 7 lines
(PAR.PA through PIG.PA) each had a stray leading `N<TAB>` (line number) baked into the actual file content
before the ticker column, e.g. `1\tPAR.PA\t...` instead of `PAR.PA\t...`. This wasn't caused by this session —
it silently existed since those rows were originally written — but it would have broken the ticker-column
completeness audit and any downstream merge. Rewrote the file with the stray prefixes stripped; verified byte-for-byte
identical content otherwise.

## Completeness audit — PASSED

Diffed all 13 tickers in `analyst_targets_PARIS_P.txt` against the P-prefixed slice of `paris_data.tsv`
(PAR.PA through PUB.PA): 0 gaps, 0 duplicates, exact match both directions.

## Final tally for group P (13/13)

3 OK (PLNW.PA, PLX.PA, PUB.PA), 10 NOFAQ. All 13 TRADEABLE. 0 blocks.

**Group P status: DONE.** Continuing sequentially to group Q per the project queue.
