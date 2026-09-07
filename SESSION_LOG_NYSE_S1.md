# Session Log — NYSE Letter S1 (S.US through SMWB, 66 tickers)

- 2026-08-27: Started fresh. Verified via `grep '^S' nyse_data.tsv | sort` — S1 = S.US through SMWB inclusive = 66 tickers, matches expected split count. Full S (132) confirmed; S2 = SN through SYY.
- 2026-08-27: Login re-verified fresh (AAPL: 314.79, "Prices by NASDAQ", Market Open, Trade button disabled:false x2). Began fetching.
- Checkpoint after 18/66 tickers (S.US through SBSI): S.US, SA, SACH, SAFE.US, SAH, SAM, SAN, SAP, SAR.US, SARO, SB, SBDS, SBH, SBMT, SBS, SBSI. 4 NOFAQ (SACH, SAN, SB, SBMT), 1 NOT_TRADEABLE (SBDS — both Trade buttons disabled). No blocks.
- Routing quirks found: bare "s" and "safe" tickers route to eToro CRYPTO pages (Sonic, Safe coin) instead of the NYSE stocks S.US (SentinelOne) and SAFE.US (Safehold Inc) — fixed by using the lowercase `.us`-suffixed URL (`s.us`, `safe.us`) which correctly resolves. Bare "sar" 404s/redirects to eToro homepage — `sar.us` works and resolves to Saratoga Investment Corp. Verified company names match nyse_data.tsv in all cases before trusting.
- Checkpoint after 28/66 tickers (S.US through SDRL): added SBSW, SCCO, SCHW, SCI, SCL, SCM, SD.US, SDHC, SDRL. 1 more NOFAQ (SD.US — double-checked with ticker=SD.US on tipranks directly since bare "sd" on eToro also routes to a crypto coin, confirmed genuinely NOFAQ). No further NOT_TRADEABLE. No blocks.
- Additional routing quirk: bare "sd" also routes to eToro crypto (Stader) — same pattern as "s"/"safe" — `sd.us` resolves correctly to SandRidge Energy Inc.
- Checkpoint after 36/66 tickers (S.US through SFL): added SE, SEAT, SEB.US, SEG, SEI.US, SES, SF.US, SFBS, SFL. 2 more NOFAQ (SEB.US, SFL — SEB.US double-checked with ticker=SEB.US on tipranks since bare "seb" 404s/redirects home). No blocks.
- More routing quirks confirmed: bare "seb", "sf" both 404/redirect to eToro home (not crypto) — `.us` suffix fixes both (Seaboard Corporation, Stifel Financial Corporation). Bare "sei" routes to crypto (Sei coin) — `sei.us` resolves to Solaris Energy Infrastructure.
- Checkpoint after 44/66 tickers (S.US through SID): added SGHC, SGI, SHAK, SHEL, SHG, SHO, SHW, SID. 2 more NOFAQ (SHG, SID). No blocks.
- Checkpoint after 48/66 tickers (S.US through SJM): added SIG, SITC, SITE, SJM. No new NOFAQ/NOT_TRADEABLE in this stretch. No blocks.
- Checkpoint after 53/66 tickers (S.US through SKY.US): added SKE, SKIL, SKM, SKT, SKY.US. 2 more NOFAQ (SKIL, SKM). Bare "sky" routes to crypto (Sky, prev Maker) — `sky.us` resolves to Skyline Champion Corporation, same routing-quirk pattern. No blocks.
- Checkpoint after 58/66 tickers (S.US through SLVM): added SLB, SLF, SLG, SLQT, SLVM. No new NOFAQ/NOT_TRADEABLE this stretch. No blocks.
- Checkpoint after 66/66 tickers (S.US through SMWB) — COMPLETE. Final stretch added SM, SMA, SMBK, SMFG, SMG, SMHI, SMP.US, SMR, SMRT, SMWB. 1 more NOFAQ (SMFG). No new NOT_TRADEABLE.
- Routing quirks in this stretch: bare "smp" 404s/redirects home — `smp.us` resolves to Standard Motor Products Inc.
- **S1 COMPLETE: 66/66 tickers fetched. Completeness audit passed (66/66, both directions match `nyse_data.tsv`'s S.US-SMWB range, no duplicates).**
- Final tally: 13 NOFAQ (SACH, SAN, SB, SBDS, SBMT, SD.US, SEB.US, SFL, SHG, SID, SKIL, SKM, SMFG), 1 NOT_TRADEABLE (SBDS — Solo Brands Inc, both Trade buttons disabled=true, also NOFAQ), 0 CVR, 53 OK/TRADEABLE.
- No blocks of any kind (login lockout, CAPTCHA, Cloudflare) encountered during the entire S1 run.
- Routing-quirk summary for S1 (useful for S2 and beyond): bare tickers "s", "safe", "sd", "sei", "sky" all route to eToro CRYPTO coins with the same symbol; bare tickers "sar", "seb", "sf", "smp" all 404/redirect to eToro home. In every case, appending `.us` (lowercase) to the ticker and using that in the `/markets/{ticker}.us/research` URL resolves correctly to the intended NYSE stock. Company name was verified against `nyse_data.tsv` in each case before trusting the match.
