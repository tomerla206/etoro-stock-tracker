import os
import subprocess
import sys
import time
import urllib.request

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
]

chrome_path = None
for path in chrome_paths:
    if os.path.exists(path):
        chrome_path = path
        break

if not chrome_path:
    print("Could not find chrome.exe path automatically.")
    sys.exit(1)

print(f"Found Chrome at: {chrome_path}")
print("Launching Chrome with --remote-debugging-port=9222 ...")

# Command to launch Chrome with remote debugging
cmd = [chrome_path, "--remote-debugging-port=9222", "https://www.etoro.com/home"]
subprocess.Popen(cmd)

time.sleep(3)

# Test CDP connection
try:
    url = "http://localhost:9222/json/version"
    req = urllib.request.urlopen(url, timeout=5)
    data = req.read().decode()
    print("[SUCCESS] CDP port 9222 is active!")
    print(data)
except Exception as e:
    print(f"[!] Failed to connect to CDP: {e}")
