import os
import sys
import time
import subprocess
import urllib.request
from playwright.sync_api import sync_playwright

print("Closing existing Chrome processes...")
subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
time.sleep(2)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

print(f"Launching Chrome with remote debugging from: {chrome_path}")
cmd = [chrome_path, "--remote-debugging-port=9222", "https://www.etoro.com/portfolio/overview"]

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

subprocess.Popen(
    cmd,
    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
    close_fds=True
)

print("Waiting for Chrome to bind CDP port 9222...")
connected = False
for _ in range(10):
    time.sleep(1)
    try:
        url = "http://localhost:9222/json/version"
        req = urllib.request.urlopen(url, timeout=2)
        if req.getcode() == 200:
            print("[SUCCESS] Connected to Chrome port 9222!")
            connected = True
            break
    except Exception:
        pass

if not connected:
    print("[!] Failed to attach to port 9222.")
    sys.exit(1)

# Now attach Playwright directly to your logged in Chrome tab!
print("\nStarting live agent on your Chrome tab...")
os.system('python run_via_cdp.py')
