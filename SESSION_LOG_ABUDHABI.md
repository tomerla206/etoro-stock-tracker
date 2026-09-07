# Abu Dhabi — Session Log

- 2026-08-29: Continuing directly from OTC Markets (72/72 done, zero blocks) in same session. Login already verified this session. Starting Abu Dhabi (29 tickers, .DH suffix), v4 method.
- Batch (tickers 1-4): 2POINTZE.DH NOFAQ TRADEABLE, ADCB.DH NOFAQ TRADEABLE, ADIB.DH NOFAQ TRADEABLE, ADNOCDIS.DH NOFAQ TRADEABLE. No blocks. 4/29 done. 100% NOFAQ so far. Resume at ticker 5, ADNOCDRI.DH.
- Batch (tickers 5-6): ADNOCDRI.DH NOFAQ TRADEABLE, ADNOCGAS.DH NOFAQ TRADEABLE. No blocks. 6/29 done. Resume at ticker 7, ADNOCLS.DH.
- Batch (tickers 7-8): ADNOCLS.DH NOFAQ TRADEABLE, ADPORTS.DH NOFAQ TRADEABLE. No blocks. 8/29 done. Resume at ticker 9, ALDAR.DH.
- Batch (tickers 9-10): ALDAR.DH NOFAQ TRADEABLE, ALPHADHA.DH NOFAQ TRADEABLE. No blocks. 10/29 done. Resume at ticker 11, AMR.DH.
- Batch (tickers 11-12): AMR.DH NOFAQ TRADEABLE, APEX.DH NOFAQ TRADEABLE. No blocks. 12/29 done. Resume at ticker 13, ASM.DH.
- Batch (tickers 13-14): ASM.DH NOFAQ TRADEABLE, BOROUGE.DH NOFAQ TRADEABLE. No blocks. 14/29 done, halfway. Resume at ticker 15, BURJEEL.DH.
- Batch (tickers 15-16): BURJEEL.DH NOFAQ TRADEABLE, EAND.DH NOFAQ TRADEABLE. No blocks. 16/29 done. Resume at ticker 17, EASYLEAS.DH.
- Batch (tickers 17-18): EASYLEAS.DH NOFAQ TRADEABLE, ESG.DH NOFAQ TRADEABLE. No blocks. 18/29 done, 11 remain. Resume at ticker 19, ESHRAQ.DH.
- Batch (tickers 19-20): ESHRAQ.DH NOFAQ TRADEABLE, FAB.DH NOFAQ TRADEABLE. No blocks. 20/29 done, 9 remain. Resume at ticker 21, IHC.DH.
- Batch (tickers 21-22): IHC.DH NOFAQ TRADEABLE, JULPHAR.DH NOFAQ TRADEABLE. No blocks. 22/29 done, 7 remain. Resume at ticker 23, LULU.DH.
- Batch (tickers 23-24): LULU.DH NOFAQ TRADEABLE, MODON.DH NOFAQ TRADEABLE. No blocks. 24/29 done, 5 remain. Resume at ticker 25, NMDC.DH.
- Batch (tickers 25-26): NMDC.DH NOFAQ TRADEABLE, PALMS.DH NOFAQ TRADEABLE. No blocks. 26/29 done, 3 remain. Resume at ticker 27, PHX.DH.
- Batch (tickers 27-29, FINAL): PHX.DH NOFAQ TRADEABLE, PRESIGHT.DH NOFAQ NOT_TRADEABLE, PUREHEAL.DH NOFAQ TRADEABLE. No blocks. **29/29 done — ABU DHABI COMPLETE.** Completeness audit: `diff <(cut -f1 abudhabi_data.tsv | sort) <(cut -f1 analyst_targets_ABUDHABI.txt | sort)` — exact match, zero gaps/duplicates. 100% NOFAQ across the entire exchange (tipranks has no coverage of ADX-listed names). Only 1 NOT_TRADEABLE (PRESIGHT.DH). Zero blocks the entire exchange, start to finish.
