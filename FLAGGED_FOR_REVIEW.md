# Flagged for Review — Lost TipRanks Coverage

**Confirmed by the user (2026-09-01)**: checked directly on eToro, these tickers genuinely have no analyst data right now. Not a scraping bug — the underlying coverage really disappeared since the original scrape.

## Group 1 — Genuinely lost aggregate analyst coverage

These previously had a real `OK` status with Low/Avg/High values; during the 2026-09-01 refresh, TipRanks showed "This stock has no research data" for each. Left unchanged (still `OK` with their last-known values) rather than auto-converted to `NOFAQ`, since a value refresh shouldn't silently erase historical data — the site's status should be updated deliberately, not as a side effect.

| Ticker | Exchange | File | Last known values (Low/Avg/High) |
|---|---|---|---|
| COCP | NASDAQ | analyst_targets_C.txt | 10.00/10.00/10.00 |
| HAFN | NYSE | analyst_targets_NYSE_H.txt | 8.47/8.47/8.47 |
| KNOP | NYSE | analyst_targets_NYSE_K.txt | 14.00/14.00/14.00 |
| MANU | NYSE | analyst_targets_NYSE_M1.txt | 30.75/30.75/30.75 |
| WPP | NYSE | analyst_targets_NYSE_W.txt | 5.91/5.91/5.91 |
| ABVX.PA | Paris | analyst_targets_PARIS_A3.txt | 136.00/163.55/187.00 |
| STB.OL | Oslo | analyst_targets_OSLO_S.txt | 150.00/177.00/216.00 |
| BAMNB.NV | Amsterdam | analyst_targets_AMSTERDAM.txt | 13.50/13.50/13.50 |
| CENER.BR | Brussels | analyst_targets_BRUSSELS.txt | 25.18/32.39/39.00 |

## Group 2 — Possible ticker/company mismatch on Yahoo (dividend scrape, different issue)

Not coverage loss — these came up during the Yahoo dividend scrape with a company name that didn't match expectations. Value was still recorded (from whatever page actually loaded), but worth a sanity check:

| Ticker | Note |
|---|---|
| NXT.US | Yahoo page resolved to "Nextpower Inc.", not the expected Nextracker. Dividend recorded as 0 either way. |
| COTY.PA | Redirected to the US Coty Inc. page rather than a Paris-specific listing. |
| PLS.ASX | Yahoo shows "PLS Group Limited" for `PLS.AX`, not "Pilbara Minerals" as expected — but the number came from the ticker's own page, so likely still correct; flagging in case Yahoo's naming is just inconsistent. |

## Why does analyst coverage appear/disappear like this?

A few real mechanisms, most likely in combination:

1. **Analysts genuinely stop covering a stock.** Coverage isn't permanent — a bank might reassign an analyst, a firm might drop coverage entirely (common when a stock's trading volume or market cap shrinks, or after negative news), or the last analyst covering it leaves/retires.
2. **Corporate events.** Mergers, going-private deals, restructurings, or major setbacks (e.g. a failed clinical trial for a biotech like ABVX.PA) can cause analysts to pull coverage quickly since their prior estimates become meaningless.
3. **Stale-rating expiry.** TipRanks' aggregate typically only counts ratings from roughly the last 3 months. If no analyst has published a fresh rating in that window, the aggregate can drop to empty even if the stock technically still has "some" historical coverage — this is the most likely explanation for small/thin-coverage names like MANU, HAFN, KNOP, STB.OL, CENER.BR, all of which likely only had one or two analysts to begin with (a single analyst going quiet is enough to zero out the whole aggregate).
4. **WPP is the one worth double-checking manually** — it's a large, well-known company (a major global ad agency), so losing ALL analyst coverage overnight would be unusual. Worth verifying directly on eToro/TipRanks that this isn't a temporary rendering glitch specific to that one ticker before treating it as a permanent loss.

**Recommendation**: leave these 9 as-is (not auto-reclassified) for now, and re-check them in a few days — if they're still empty, it's safe to convert them to genuine `NOFAQ` status. If any come back with coverage, it confirms option 3 (stale-rating cycling) rather than a permanent drop.
