# Session Log — Frankfurt letter A (39 tickers)

2026-08-26: Started immediately after finishing group 0-9 (14/14 done). Same dedicated tab lineage — original tab 1160639712 started timing out on screenshot/page-text after ~23 fetches (known Claude-in-Chrome issue per PROJECT_LOG), replaced with fresh tab 1160639748 mid-letter (opened new tab, closed broken one) — no block, just the known screenshot-timeout quirk. Continuing to see occasional unrelated tabs from the other (NYSE?) agent appear/disappear in the tab group (Paris-exchange tickers like AB.PA, ABCA.PA, ABEO.PA, ABNX.PA, ABVX.PA) — never touched, per dual-agent policy.

Progress (checkpoint at 14/39):
- A1OS.DE (All for One Group SE) — 68.00, NOFAQ, TRADEABLE
- A4Y0.DE (Accentro Real Estate AG) — 37.600, NOFAQ, NOT_TRADEABLE
- A6T.DE (Artec Technologies AG) — 2.050, NOFAQ, TRADEABLE
- A7A.DE (Heliad AG) — 14.20, NOFAQ, TRADEABLE
- AAD.DE (AMADEUS FIRE AG) — 21.15, NOFAQ, TRADEABLE
- AAG.DE (AUMANN AG) — 14.55, NOFAQ, TRADEABLE
- AAPL.EUR (Apple) — 265.20, NOFAQ (tipranks widget doesn't recognize .EUR-suffixed CFD ticker, expected), TRADEABLE
- AAQ1.DE (Aap Implantate AG) — 1.400, NOFAQ, TRADEABLE
- ABO.DE (Clearvise AG) — 1.030, NOFAQ, TRADEABLE
- ABS2.DE (Porr AG) — 39.80, Low 42.00/Avg 42.00/High 42.00, OK, TRADEABLE
- ABX.DE (Advanced Blockchain AG) — 1.100, NOFAQ, TRADEABLE
- ACT.DE (Alzchem Group AG) — 161.50, Low 200.00/Avg 203.00/High 208.00, OK, TRADEABLE
- ACWN.DE (AS Creation Tapeten AG) — 6.80, NOFAQ, TRADEABLE

- ACX.DE (bet at home com AG) — 3.260, NOFAQ, TRADEABLE
- ADE.DE (Bitcoin Group SE) — 27.80, NOFAQ, TRADEABLE
- ADJ.DE (ADO Properties SA) — 0.1295, NOFAQ, TRADEABLE

## BLOCK HIT — 2026-08-26, on ADN1.DE

Got Low/Avg/High from tipranks widget for ADN1.DE (Hold, 1 analyst, Low 65.00/Avg 65.00/High 65.00 — NOT yet written to output file since price/tradeability couldn't be confirmed). Navigated to `https://www.etoro.com/markets/adn1.de/research` for the price+tradeability leg and hit the **ordinary lockout signature**: price line showed "Delayed prices by Xetra, in EUR" (not real-time), Analysis tab showed "Research information is only available to active investors / Sign up" gate, and a screenshot confirmed: "It looks like something went wrong" dialog + left sidebar flipped to logged-out ("Have an account? / Sign in", "Sign up" button at bottom) — textbook match for signature 1 in PROJECT_LOG.md's block-handling section.

Stopped immediately per protocol — did not retry, did not attempt to log in. **Resume point: ADN1.DE** (needs a fresh price+tradeability fetch once login clears; the Low/Avg/High 65.00/65.00/65.00 already captured above can be reused, just re-verify AnalysisStatus=OK still holds).

Remaining after ADN1.DE: ADS.DE, ADV.DE, AEIN.DE, AFX.DE, AG1.DE, AGB2.DE, AIXA.DE, AJ91.DE, ALG.DE, ALI1.DE, ALV.DE, AMD.EUR, AMI.DE, AMM.DE, AMV0.DE, AMZN.EUR, AOF.DE, APM.DE, AT1.DE, AUS.DE, AVGO.EUR, AZ2.DE (22 left, 23 including ADN1.DE itself).

Checkpoint: 16/39 letter-A tickers written to `analyst_targets_FRANKFURT_A.txt` (verified — file has 16 lines as of this stop). Plus the completed 0-9 group (14/14).

**User action needed to clear this**: per PROJECT_LOG.md, this type of block does not reliably clear just by waiting — needs a genuine user re-login (or in worse cases a router/modem power-cycle for a fresh IP). Reporting back now rather than retrying blindly.

## RESUMED 2026-08-26 — fresh login re-verified, ADN1.DE redone, then SECOND block hit on AGB2.DE

Re-verified eToro login myself (AAPL: 309.45 real-time off-hours price, "Prices by NASDAQ", Trade disabled:false) before starting — confirmed clean. Used dedicated fresh tab (tabId 1160639766, own tab group since the prior one had been closed). Noted other agents' tabs (Paris/ASX/Stockholm tickers) cycling in/out of the same tab group throughout — never touched, per policy.

Redid ADN1.DE completely fresh: tipranks Low/Avg/High 65.00/65.00/65.00 re-confirmed identical, eToro side now clean (57.50, "Market Open", Trade disabled:false) — block had cleared. Written to output file.

Continued and completed 6 more tickers cleanly: ADS.DE, ADV.DE, AEIN.DE, AFX.DE, AG1.DE — batch of 7 total (incl. ADN1.DE) went through without issue, paced 3-6s per ticker.

**Hit a SECOND ordinary lockout on AGB2.DE** (2026-08-26, same session): tipranks widget gave NOFAQ (not yet written, price/tradeability unconfirmed — same policy as the first ADN1.DE block). eToro `/markets/agb2.de/research` showed: price label "Delayed prices by Xetra, in EUR" (not real-time), and a screenshot confirmed the **exact signature-1 match**: "It looks like something went wrong" / "Don't worry, this is probably a temporary issue. Please refresh to reload your details." dialog, plus left sidebar flipped to logged-out ("Have an account? / Sign in", "Sign up" button at bottom). Stopped immediately, did not retry/refresh/log in.

**Resume point: AGB2.DE** (tipranks NOFAQ already known and reusable, just needs a fresh price+tradeability check once login clears).

Remaining after AGB2.DE: AIXA.DE, AJ91.DE, ALG.DE, ALI1.DE, ALV.DE, AMD.EUR, AMI.DE, AMM.DE, AMV0.DE, AMZN.EUR, AOF.DE, APM.DE, AT1.DE, AUS.DE, AVGO.EUR, AZ2.DE (16 left, 17 including AGB2.DE itself).

Checkpoint: 22/39 letter-A tickers written to `analyst_targets_FRANKFURT_A.txt` (16 carried over + ADN1.DE + ADS.DE + ADV.DE + AEIN.DE + AFX.DE + AG1.DE = 22).

**Two ordinary-lockout blocks in one session on the same letter, both with the account genuinely re-logged-in beforehand** — this may indicate the shared-account/parallel-agent load (up to 5 simultaneous agents across exchanges) is triggering these more often than the single-agent baseline. Worth flagging to the user/coordinator. Same fix needed: genuine re-login or router/modem power-cycle for a fresh IP — does not reliably clear on its own.

## RESUMED 2026-08-26 — new session after quota reset, ADN1.DE/AGB2.DE blocks had cleared, THIRD block hit on AMI.DE

New session (prior one had run out of shared usage quota mid-letter, not a block — per the coordinating session's own checkpoint verification, file had 26/39 rows, last ALG.DE). Verified eToro login myself before starting: navigated to `https://www.etoro.com/markets/aapl/research` on a dedicated fresh tab (never touched other agents' tabs, which were cycling through Stockholm/Paris/ASX tickers in the shared tab group throughout — ARJOb.ST, ALATA.PA, AUB.ASX, ALTRA.ST, AMBEA.ST, AX1.ASX, ANODb.ST, ALBFR.PA, AZJ.ASX, etc.) — confirmed clean: 310.30 real-time off-hours price, "Prices by NASDAQ", Trade disabled:false.

Completed 3 more tickers cleanly, paced 2-6s per ticker:
- ALI1.DE (Almonty Industries Inc) — 15.8750, Low 19.71/Avg 20.57/High 21.42, OK, TRADEABLE
- ALV.DE (Allianz SE) — 452.40, Low 325.00/Avg 460.67/High 684.00, OK, TRADEABLE
- AMD.EUR (Advanced Micro Devices Inc) — 408.15, NOFAQ, TRADEABLE

**Hit a THIRD ordinary lockout on AMI.DE** (2026-08-26): tipranks widget gave NOFAQ (not yet written, price/tradeability unconfirmed — same policy as prior blocks). eToro `/markets/ami.de/research` showed price 0.171 with "Delayed prices by Xetra, in EUR" label, and an Analysis-tab gate ("Research information is only available to active investors / Sign up"). Took a screenshot to confirm before treating it as a real block (this ticker's "delayed prices" alone could in principle just be a genuine illiquid-microcap quirk) — screenshot confirmed the **exact signature-1 match**: "It looks like something went wrong" / "Don't worry, this is probably a temporary issue. Please refresh to reload your details." modal dialog, plus left sidebar flipped fully to logged-out ("Have an account? / Sign in" + "Sign up" button at bottom, Home/Watchlist/Portfolio/Discover nav instead of account menu). Stopped immediately, did not click "Try Again", did not attempt to log in.

**Resume point: AMI.DE** (tipranks NOFAQ already known and reusable, just needs a fresh price+tradeability check once login clears).

Remaining after AMI.DE: AMM.DE, AMV0.DE, AMZN.EUR, AOF.DE, APM.DE, AT1.DE, AUS.DE, AVGO.EUR, AZ2.DE (9 left, 10 including AMI.DE itself).

Checkpoint: 29/39 letter-A tickers written to `analyst_targets_FRANKFURT_A.txt` (verified — file has 29 lines as of this stop; 26 carried over + ALI1.DE + ALV.DE + AMD.EUR = 29).

**Third ordinary-lockout block on this same letter across sessions, again with a freshly-verified clean login immediately beforehand.** Consistent with the parallel-agent-load theory noted above. Per protocol: this does not reliably clear on its own — needs a genuine user re-login, or in tougher cases a router/modem power-cycle for a fresh IP. Reporting back now rather than retrying blindly.

## RESUMED 2026-08-28 — strict sequential mode now in effect (sole active agent, project-wide policy change), block had cleared, LETTER A COMPLETED

Per the 2026-08-26 "Policy update" in `PROJECT_LOG.md`, the whole project family is back to one-agent-at-a-time across ALL exchanges (the earlier 5-way parallel run caused this letter's repeated blocks). Re-verified eToro login fresh on a dedicated new tab before starting: AAPL 314.64 real-time, Off-hours, "Prices by NASDAQ", Trade disabled:false, previous close normal — clean.

Redid AMI.DE completely fresh: tipranks NOFAQ re-confirmed, eToro side now clean (0.151, "Market Closed"/"Prices by Xetra, in EUR" — normal, not "Delayed prices" — Trade disabled:false). Block had cleared. Written to output file.

Completed the remaining 9 tickers cleanly, paced ~2-6s per ticker, no issues:
- AMM.DE (Grounds Real Estate Development AG) — 0.150, NOFAQ, NOT_TRADEABLE (Trade disabled:true)
- AMV0.DE (Aumovio SE) — 34.70, Low 46.40/Avg 51.13/High 60.00, OK, TRADEABLE
- AMZN.EUR (Amazon.com Inc) — 220.65, NOFAQ, TRADEABLE
- AOF.DE (ATOSS SOFTWARE AG) — 100.00, Low/Avg/High 115.00/115.00/115.00, OK, TRADEABLE
- APM.DE (Ad Pepper Media International NV) — 2.56, NOFAQ, TRADEABLE
- AT1.DE (Aroundtown SA) — 2.0120, Low 2.70/Avg 3.25/High 3.80, OK, TRADEABLE
- AUS.DE (AT & S Austria Technologie & Systemtechnik AG) — 148.40, Low/Avg/High 320.00/320.00/320.00, OK, NOT_TRADEABLE (Trade disabled:true)
- AVGO.EUR (Broadcom Inc) — 318.25, NOFAQ, TRADEABLE
- AZ2.DE (Andritz AG) — 81.80, Low/Avg/High 93.00/93.00/93.00, OK, TRADEABLE (tipranks "Top Analysts" view based on 1 ranked analyst — visually confirmed via screenshot since a second listed analyst had a different 92.00 target not included in the ranked figure)

**Letter A complete: 39/39.** Completeness audit run: diffed all `^A` tickers in `frankfurt_data.tsv` against `analyst_targets_FRANKFURT_A.txt`, both directions — 0 gaps, 0 extras, both files have exactly 39 matching tickers. No blocks hit this session. Zero blocks in strict-sequential mode vs. three in the earlier parallel-run period — supports the parallel-load theory from before.

Moving on to letter B per the coordinating session's instructions — see `SESSION_LOG_FRANKFURT_B.md`.
