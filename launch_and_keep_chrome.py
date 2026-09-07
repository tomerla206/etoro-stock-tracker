import os
import subprocess
import sys
import time
import urllib.request

profile_dir = os.path.expanduser(r"~\.chrome_debug_profile")
os.makedirs(profile_dir, exist_ok=True)

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
]

chrome_path = None
for p in chrome_paths:
    if os.path.exists(p):
        chrome_path = p
        break

if not chrome_path:
    print("Chrome not found")
    sys.exit(1)

print(f"Launching Chrome from {chrome_path} with profile {profile_dir}...")
cmd = [
    chrome_path,
    f"--user-data-dir={profile_dir}",
    "--remote-debugging-port=9222",
    "https://www.etoro.com/home"
]

proc = subprocess.Popen(cmd)

for _ in range(15):
    time.sleep(1)
    try:
        url = "http://localhost:9222/json/version"
        req = urllib.request.urlopen(url, timeout=2)
        if req.getcode() == 200:
            print("[SUCCESS] Chrome CDP port 9222 is ONLINE!")
            print(req.read().decode())
            sys.exit(0)
    except Exception:
        pass

print("[!] Chrome failed to bind port 9222")
sys.exit(1)
