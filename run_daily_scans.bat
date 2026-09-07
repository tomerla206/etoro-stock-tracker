@echo off
cd /d "%~dp0"
echo ===== Daily scan started: %date% %time% ===== >> daily_scan_run.log
echo Running MEGASCAN (TipRanks, ~50 min)...
python megascan.py >> daily_scan_run.log 2>&1
echo Running MEGASCAN YAHOO (~3 hours)...
python megascan_yahoo.py >> daily_scan_run.log 2>&1
echo ===== Daily scan finished: %date% %time% ===== >> daily_scan_run.log
