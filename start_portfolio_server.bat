@echo off
cd /d "%~dp0"
echo Starting portfolio server...
echo Once it says "Serving on http://localhost:8791/nasdaq-stocks.html", open that link in your browser.
python portfolio_server.py
pause
