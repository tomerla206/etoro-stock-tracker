# Portfolio Refresh Log

Refreshing analyst Low/Avg/High (TipRanks widget) + Yahoo dividend yield for the 55 tickers in `portfolio_scan_list.txt`.

### Batch 1 (tickers 1-21)
- ALLO | analyst: unchanged (10.00/12.00/14.00) | dividend: 0%
- ALNY | analyst: unchanged (230.00/397.59/550.00) | dividend: 0%
- AMTX | analyst: unchanged (28.00/28.00/28.00) | dividend: 0%
- ASLE | analyst: unchanged (7.00/7.25/7.50) | dividend: 0%
- AVNW | analyst: unchanged (30.00/33.60/38.00) | dividend: 0%
- AZO | analyst: unchanged (4325.00/4325.00/4325.00) | dividend: 0%
- BABA | analyst: unchanged (160.00/188.42/220.10) | dividend: 0.88%
- BLK | analyst: unchanged (1144.00/1299.00/1450.00) | dividend: 1.97%
- CABA | analyst: unchanged (16.00/23.00/30.00) | dividend: 0%
- CAN | analyst: unchanged (3.00/3.00/3.00) | dividend: 0%
- CBRE | analyst: unchanged (174.00/181.33/190.00) | dividend: 0%
- CBUS | analyst: unchanged (25.00/25.00/25.00) | dividend: 0%
- CIFR | analyst: unchanged (22.00/30.72/43.50) | dividend: 0%
- COF | analyst: unchanged (222.00/259.56/300.00) | dividend: 1.48%
- CRBU | analyst: unchanged (5.00/8.00/11.00) | dividend: 0%
- DIS | analyst: unchanged (111.00/127.08/137.00) | dividend: 1.39%
- EXPN.L | analyst: unchanged (3812.00/3906.00/4000.00) | dividend: 1.70%
- FICO | analyst: unchanged (1200.00/1531.00/1700.00) | dividend: 0%
- GE | analyst: unchanged (380.00/416.10/455.00) | dividend: 0.55%
- HIVE | analyst: unchanged (6.00/7.25/10.00) | dividend: 0%
- IVVD | analyst: unchanged (10.00/10.00/10.00) | dividend: 0%
- KLAC | analyst: unchanged (180.00/241.89/325.00) | dividend: 0.52%
- LCTX | analyst: unchanged (9.00/9.00/9.00) | dividend: 0%
- LENZ | analyst: unchanged (7.00/24.40/60.00) | dividend: 0%
- LSCC | analyst: unchanged (160.00/167.11/180.00) | dividend: 0%
- MA | analyst: unchanged (550.00/664.42/740.00) | dividend: 0.58%

Progress: 26/55 done. All analyst values already matched current file data (no edits needed so far); dividends newly recorded for all.

### Batch 2 (tickers 27-45)
- MANU | analyst: TipRanks shows "This stock has no research data" now — file still has 30.75/30.75/30.75, left UNCHANGED per instructions | dividend: 0%
- NEM.DE | analyst: unchanged (52.00/86.75/115.00) | dividend: 0.96%
- NJR | analyst: unchanged (61.00/62.50/64.00) | dividend: 3.54%
- NKTX | analyst: unchanged (10.00/11.67/14.00) | dividend: 0%
- NOK | analyst: unchanged (15.00/17.75/21.00) | dividend: 1.60%
- NOVT | analyst: unchanged (194.00/194.00/194.00) | dividend: 0%
- NVT | analyst: unchanged (191.00/205.17/215.00) | dividend: 0.57%
- OCGN | analyst: unchanged (10.00/10.50/11.00) | dividend: 0%
- PCVX | analyst: unchanged (75.00/104.60/133.00) | dividend: 0%
- PLNT | analyst: unchanged (51.00/64.43/82.00) | dividend: 0%
- PRQR | analyst: unchanged (8.00/9.60/12.00) | dividend: 0%
- PTCT | analyst: unchanged (70.00/99.56/130.00) | dividend: 0%
- RHM.DE | analyst: unchanged (1350.00/1650.00/2300.00) | dividend: 1.00%
- RL | analyst: unchanged (425.00/460.44/520.00) | dividend: 1.13%
- RYTM | analyst: unchanged (105.00/138.58/160.00) | dividend: 0%

Progress: 41/55 done.

### Batch 3 (tickers 42-52)
- SKHY | analyst: unchanged (200.00/248.00/320.00) | dividend: 0%
- STC | analyst: unchanged (71.00/79.00/87.00) | dividend: 3.00%
- SURG | analyst: unchanged (3.50/3.50/3.50) | dividend: 0%
- TCRX | analyst: unchanged (5.00/6.00/7.00) | dividend: 0%
- TM | analyst: TipRanks "no research data" — file already NOFAQ with blank Low/Avg/High, left UNCHANGED | dividend: 3.22%
- TNYA | analyst: unchanged (3.00/13.00/40.00) | dividend: 0%
- TTWO | analyst: unchanged (270.00/299.45/368.00) | dividend: 0%
- UBER | analyst: unchanged (89.00/104.73/119.00) | dividend: 0%
- UPB | analyst: unchanged (9.00/36.25/75.00) | dividend: 0%
- V | analyst: unchanged (350.00/422.67/460.00) | dividend: 0.70%
- VOD | analyst: TipRanks "no research data" — file already NOFAQ with blank Low/Avg/High, left UNCHANGED | dividend: 3.35%

Progress: 52/55 done.

### Batch 4 (tickers 53-55, final)
- VST | analyst: unchanged (169.00/228.00/298.00) | dividend: 0.67%
- WMT | analyst: unchanged (110.00/127.43/155.00) | dividend: 0.94%
- WYNN | analyst: unchanged (128.00/136.50/145.00) | dividend: 1.05%

Progress: 55/55 done. ALL COMPLETE.

## Summary
- All 55 tickers checked against the TipRanks widget. In every case except MANU/TM/VOD, the widget's Low/Avg/High matched the value already stored in the source `analyst_targets_*.txt` file exactly (to 2 decimals) — no edits were required to any analyst_targets file this pass.
- MANU, TM, VOD: TipRanks widget returned "This stock has no research data" — files already carry NOFAQ status (TM, VOD) or a prior aggregate (MANU); left untouched per instructions, noted here.
- Dividend yields for all 55 tickers newly recorded in `yahoo_dividends_PORTFOLIO.txt` (created this session).
- Next: run `merge_yahoo_dividends.py` and `merge_analyst_targets.py`, then reassemble `nasdaq-stocks.html`.

