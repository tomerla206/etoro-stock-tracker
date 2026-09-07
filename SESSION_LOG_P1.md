# Session Log — Letter P1 (NASDAQ v3)

Scope: first 53 of 107 alphabetically-sorted P-tickers, PAA through PLSE inclusive.

## 2026-08-24
- Started fresh. Read PROJECT_LOG.md, LETTER_STATUS.md, nasdaq_data.tsv.
- Confirmed via sort: 107 total P-tickers; PLSE is exactly the 53rd alphabetically. P1 list:
  PAA, PAAS, PACB, PAGP, PAHC, PANL, PATK, PAX, PAYO, PAYP, PAYS, PAYX, PBLS, PBYI, PCAR, PCT.US, PCTY, PCVX, PCYO, PDD, PDFS, PDLB, PDSB, PEBO, PECO, PEGA, PENG, PENN, PEP, PERI, PESI, PETS.US, PFBC, PFG, PFIS, PFLT, PGC, PGNY, PGY, PHAT, PHUN, PHVS, PI, PICS, PIII, PKOH, PLAB, PLAY, PLCE, PLMR, PLPC, PLRX, PLSE
- No pre-existing analyst_targets_P1.txt or SESSION_LOG_P1.md.
- Verified eToro login clean (AAPL check: Tomer Lalo Schwartz, green Trade, Prices by NASDAQ, 245.00/337.09/400.00).
- Batch 1 (13): PAA-PBLS. All OK/TRADEABLE except PAHC, PAX (NOFAQ/TRADEABLE). No blocks.
- Batch 2 (13): PBYI-PEGA. All OK/TRADEABLE except PCT.US, PCYO, PDLB (NOFAQ/TRADEABLE). No blocks.
- Checkpoint: 26/53 done, resume at PENG next. No NOT_TRADEABLE, no CVR, no MISMATCH so far.
- Batch 3 (12 of planned 13): PENG-PGNY completed OK/TRADEABLE (PETS.US, PFIS NOFAQ/TRADEABLE). Total 38/53 done.
- **BLOCKED at PGY** (39th ticker): navigated to https://www.etoro.com/markets/pgy/research and got the ordinary-lockout signature — "It looks like something went wrong" dialog, sidebar flipped to logged-out ("Have an account? / Sign in"), price shows "Delayed prices by NASDAQ". Per protocol: stopped immediately, did NOT retry, did NOT attempt login. Last fully completed ticker: PGNY. Next ticker to do on resume: PGY (re-verify login first per protocol, then redo PGY since it wasn't captured).
- Exceptions so far (all TRADEABLE): PAHC, PAX, PCT.US, PCYO, PDLB, PETS.US, PFIS = NOFAQ. 0 NOT_TRADEABLE, 0 CVR, 0 MISMATCH, 0 NEW.

## Resume session (same day, later)
- Diffed analyst_targets_P1.txt (38 rows) against the confirmed sorted 53-ticker P1 list before starting — matched the logged checkpoint exactly (resume at PGY), no stale-log gap this time.
- Re-verified eToro login clean: Tomer Lalo Schwartz, green Trade, Prices by NASDAQ, AAPL 245.00/337.09/400.00.
- Batch 4 (15, completes P1): PGY-PLSE all done, all TRADEABLE. New exception: PHUN = NOFAQ (also TRADEABLE). No blocks this session.
- **P1 COMPLETE: 53/53.** Total exceptions across whole letter: 0 NEW, 0 MISMATCH, 0 NOT_TRADEABLE, 0 CVR, 8 NOFAQ (PAHC, PAX, PCT.US, PCYO, PDLB, PETS.US, PFIS, PHUN — all still TRADEABLE despite no research data).
- Completeness audit run: diffed final 53-ticker target list against analyst_targets_P1.txt both directions — 53/53, zero mismatch either way.
