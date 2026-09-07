@echo off
cd /d "%~dp0"
echo ===== Daily pull started: %date% %time% ===== >> daily_scan_run.log
echo Pulling fresh scan results from GitHub (MEGASCAN/MEGASCAN YAHOO/INSIDER SCAN/FUNDAMENTALS SCAN now run in the cloud - see .github/workflows/daily-scan.yml)...
python pull_and_merge.py >> daily_scan_run.log 2>&1
echo ===== Daily pull finished: %date% %time% ===== >> daily_scan_run.log
