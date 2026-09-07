# Session Log — Frankfurt Letter H

2026-08-28: Started immediately after letter G completed (same session, login already verified).

Batch 1 (5/25): H2O.DE, H9W.DE, HABA.DE, HAG.DE, HAW.DE — all done cleanly.

**BLOCK HIT on HBH.DE (6th ticker), 2026-08-28.** Signature: CAPTCHA — "Verification Required" / "Slide right to secure your access", page explicitly cites "Automated (bot) activity on your network (IP 46.121.145.58)" plus "Rapid taps or clicks" / "JavaScript disabled or not working" / "Use of developer or inspection tools" as possible reasons. Challenge ID: e2ef290a-fd53-8dd7-5ae5-3a4c6dff20c3.

Earliest visible symptom: the HBH.DE etoro research page came back showing "Delayed prices by Xetra" (not real-time) and a "Research information is only available to active investors / Sign up" gate on the Analysis panel, with the Trade-button JS check returning 4 buttons instead of the usual 2 (page structure had changed) — this was the tell that something was already wrong before the full CAPTCHA screen was confirmed via a direct AAPL re-check.

HBH.DE's fetched tipranks data (Low 90.00 / Avg 91.00 / High 92.00) was captured before the block was confirmed but is NOT recorded in the output file — discarded as unreliable/unverifiable given the block. HBH.DE must be redone cleanly from scratch once login is restored.

Per protocol: stopped immediately, did not attempt to solve/retry the CAPTCHA, did not attempt to log in. Reported back to the user/coordinating session. The block does not reliably clear just by waiting — user needs to disconnect the internet and power-cycle the router/modem for a fresh IP.

Resume point: HBH.DE (6th of 25) — redo from scratch once login is verified fresh again (AAPL check: real-time price, "Prices by NASDAQ" not "Delayed", Trade button enabled, no CAPTCHA/lockout).

Tally so far (5 done): 2 OK (HABA.DE, HAG.DE), 3 NOFAQ (H2O.DE, H9W.DE, HAW.DE), 0 NOT_TRADEABLE, 0 CVR.

**RESUMED 2026-08-28** (new session, strict sequential mode, login re-verified fresh via AAPL check: real-time "Prices by NASDAQ", Off-hours, Trade disabled:false x2 — no CAPTCHA). HBH.DE redone completely fresh (tipranks + eToro) — data matched the pre-block read exactly (Low 90.00/Avg 91.00/High 92.00), confirming it wasn't corrupted, but recorded only from this fresh pass per protocol.

Batch 2 (16/25 total): HBH.DE (OK), HDD.DE (OK), HEI.DE (OK), HEN.DE (NOFAQ), HEN3.DE (OK), HFG.DE (OK), HGEA.DE (NOFAQ), HIGH.DE (NOFAQ), HLAG.DE (OK), HLE.DE (OK), HLG.DE (NOFAQ) — zero blocks, zero issues.

Tally at 16/25: 9 OK, 7 NOFAQ, 0 NOT_TRADEABLE, 0 CVR/MISMATCH.

Remaining (9): HMU.DE, HNL.DE, HNR1.DE, HOT.DE, HP3A.DE, HPHA.DE, HRPK.DE, HTG.DE, HYQ.DE.

**LETTER H COMPLETE (25/25), 2026-08-28.** Finished remaining 9: HMU.DE (NOFAQ), HNL.DE (NOFAQ), HNR1.DE (OK), HOT.DE (OK), HP3A.DE (NOFAQ), HPHA.DE (NOFAQ), HRPK.DE (NOFAQ), HTG.DE (NOFAQ), HYQ.DE (OK). Zero blocks entire resumed session (20 tickers fetched: HBH.DE redo + 19 new).

Final tally (25/25): 11 OK, 14 NOFAQ, 0 NOT_TRADEABLE, 0 CVR/MISMATCH.

Completeness audit: `diff` of ticker column vs `grep '^H' frankfurt_data.tsv` — 0 gaps, 0 extras. PASSED.
