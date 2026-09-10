"""
Local server for the stock site + on-demand scan buttons.

Run: python portfolio_server.py
Then open http://localhost:8791/nasdaq-stocks.html

Each button on the page (Scan Values / MEGASCAN / MEGASCAN YAHOO / Insider Scan /
Pull Updates) POSTs to /run/<name>, which launches that scan's script as its
own background subprocess (non-blocking - the server stays responsive to
other requests while a multi-hour scan runs, thanks to ThreadingTCPServer).
GET /status polls each scan's own progress-log file plus whether its process
is still alive, so the page can show live progress/ETA and a "last completed"
timestamp without ever blocking on a running scan.

"Pull Updates" (name "pull", see pull_and_merge.py) is also POSTed once
automatically by the page's own JS right after it loads - the fastest way
for opening the site to actually pick up fresh cloud-scanned data is to just
ask this server to git-pull-and-rebuild the moment the page opens, instead of
only ever relying on the once-a-day Scheduled Task.

SCAN HOLDINGS and SCAN RED are NOT here and never will be - they require a
live Claude session driving a real logged-in eToro browser session, which no
local script can do unattended.
"""

import gzip
import http.server
import json
import mimetypes
import re
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).parent
PORT = 8791

# Text-based file types worth gzip-compressing before sending - nasdaq-stocks.html
# is ~27MB and compresses to a fraction of that, cutting download time a lot on
# a first visit (this doesn't speed up the browser's HTML parsing itself, only
# the network transfer beforehand).
COMPRESSIBLE_EXTS = {".html", ".htm", ".js", ".css", ".json", ".txt", ".tsv", ".md", ".csv"}

# name -> (script, progress-log file, results file or None)
SCANS = {
    "scan_values": ("scan_values.py", "SCAN_VALUES_LOG.md", None),
    "megascan": ("megascan.py", "MEGASCAN_LOG.md", "MEGASCAN_RESULTS.md"),
    "megascan_yahoo": ("megascan_yahoo.py", "MEGASCAN_YAHOO_LOG.md", "MEGASCAN_YAHOO_RESULTS.md"),
    "insider_scan": ("insider_scan.py", "INSIDER_SCAN_LOG.md", "INSIDER_SCAN_RESULTS.md"),
    "fundamentals_scan": ("fundamentals_scan.py", "FUNDAMENTALS_SCAN_LOG.md", "FUNDAMENTALS_SCAN_RESULTS.md"),
    # git pull + rebuild from the cloud's latest scan results (normally run
    # once a day by a Scheduled Task) - also runnable on demand, and
    # auto-triggered once per page load, so opening the site can pick up
    # fresh cloud data without waiting for that daily task. Same
    # log-file-driven "last: Xh ago" status as every scan above, just with
    # PULL_LOG.md standing in for both the progress log and the results file
    # (see pull_and_merge.py - it's a single summary line, not a scan with
    # a Done/Total to track).
    "pull": ("pull_and_merge.py", "PULL_LOG.md", "PULL_LOG.md"),
}

_GZIP_CACHE = {}  # rel_path -> (mtime, compressed_bytes) - nasdaq-stocks.html is
# ~45MB, so recompressing it on every single request (every reload/tab-open)
# burns real CPU for no reason when the file hasn't changed since last serve.

RUNNING = {}  # name -> subprocess.Popen, only tracks processes started by THIS server run
RUNNING_LOCK = threading.Lock()  # ThreadingServer handles requests on separate
# threads, so two near-simultaneous POST /run/<name> requests (e.g. a
# double-click) could both pass the "already running" check before either
# writes to RUNNING, launching the same scan script twice concurrently.


def parse_log(name):
    script, log_file, results_file = SCANS[name]
    log_path = ROOT / log_file
    info = {"done": None, "total": None, "eta_min": None, "log_age_sec": None}

    if log_path.exists():
        text = log_path.read_text(encoding="utf-8")
        m = re.search(r"Done:\s*(\d+)\s*/\s*(\d+)", text)
        if m:
            info["done"], info["total"] = int(m.group(1)), int(m.group(2))
        m = re.search(r"ETA:\s*([\d.]+)\s*min", text)
        if m:
            info["eta_min"] = float(m.group(1))
        info["log_age_sec"] = time.time() - log_path.stat().st_mtime

    proc = RUNNING.get(name)
    still_running_tracked = proc is not None and proc.poll() is None
    if proc is not None and proc.poll() is not None:
        del RUNNING[name]

    # Fallback for scans started outside this server process (e.g. the
    # scheduled Windows Task, or a manual `python megascan.py` run): infer
    # "probably running" from the log file being touched very recently while
    # not yet at 100%.
    inferred_running = (
        not still_running_tracked
        and info["log_age_sec"] is not None
        and info["log_age_sec"] < 120
        and info["done"] is not None
        and info["total"] is not None
        and info["done"] < info["total"]
    )
    info["running"] = still_running_tracked or inferred_running

    results_path = ROOT / results_file if results_file else log_path
    info["last_completed"] = None
    if results_path.exists() and not info["running"]:
        info["last_completed"] = results_path.stat().st_mtime

    return info


def start_scan(name):
    script = SCANS[name][0]
    with RUNNING_LOCK:
        existing = RUNNING.get(name)
        if existing is not None and existing.poll() is None:
            return {"status": "already_running"}
        proc = subprocess.Popen(
            [sys.executable, script], cwd=ROOT,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        RUNNING[name] = proc
    return {"status": "started"}


class Handler(http.server.SimpleHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path.startswith("/run/"):
            name = self.path[len("/run/"):]
            if name not in SCANS:
                return self._json({"status": "error", "message": f"unknown scan '{name}'"}, 404)
            try:
                self._json(start_scan(name))
            except Exception as e:
                self._json({"status": "error", "message": str(e)}, 500)
        elif self.path == "/scan-portfolio":
            # legacy path, same as /run/scan_values
            try:
                self._json(start_scan("scan_values"))
            except Exception as e:
                self._json({"status": "error", "message": str(e)}, 500)
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == "/status":
            try:
                self._json({name: parse_log(name) for name in SCANS})
            except Exception as e:
                self._json({"status": "error", "message": str(e)}, 500)
        elif self._try_serve_gzip():
            pass
        else:
            super().do_GET()

    def _try_serve_gzip(self):
        """Serve compressible files gzip-encoded when the browser supports it
        (virtually always). Falls back to the normal (uncompressed) path -
        returns False - for anything not eligible, so this can never break a
        request, only speed some of them up."""
        if "gzip" not in self.headers.get("Accept-Encoding", ""):
            return False
        parsed = urlparse(self.path)
        rel_path = unquote(parsed.path).lstrip("/")
        if not rel_path or parsed.path.endswith("/"):
            return False
        if Path(rel_path).suffix.lower() not in COMPRESSIBLE_EXTS:
            return False
        file_path = ROOT / rel_path
        try:
            if not file_path.is_file():
                return False
            mtime = file_path.stat().st_mtime
        except OSError:
            return False

        cached = _GZIP_CACHE.get(rel_path)
        if cached is not None and cached[0] == mtime:
            compressed = cached[1]
        else:
            try:
                data = file_path.read_bytes()
            except OSError:
                return False
            compressed = gzip.compress(data, compresslevel=6)
            _GZIP_CACHE[rel_path] = (mtime, compressed)

        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(compressed)))
        self.send_header("Last-Modified", self.date_time_string(int(mtime)))
        self.end_headers()
        self.wfile.write(compressed)
        return True

    def log_message(self, fmt, *args):
        print(fmt % args)


if __name__ == "__main__":
    import os

    os.chdir(ROOT)

    class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True

    with ThreadingServer(("", PORT), Handler) as httpd:
        print(f"Serving on http://localhost:{PORT}/nasdaq-stocks.html")
        print("Scan endpoints: POST /run/scan_values, /run/megascan, /run/megascan_yahoo, /run/insider_scan")
        print("Status endpoint: GET /status")
        httpd.serve_forever()
