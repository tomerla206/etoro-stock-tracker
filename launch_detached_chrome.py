import os
import subprocess
import time
import urllib.request

profile_dir = os.path.expanduser(r"~\.chrome_debug_profile")
os.makedirs(profile_dir, exist_ok=True)

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_exe):
    chrome_exe = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

print("Starting detached Chrome process...")
ps_cmd = f"Start-Process '{chrome_exe}' -ArgumentList '--user-data-dir={profile_dir}', '--remote-debugging-port=9222', 'https://www.etoro.com/home'"

subprocess.run(["powershell", "-Command", ps_cmd])

for i in range(10):
    time.sleep(1)
    try:
        url = "http://localhost:9222/json/version"
        req = urllib.request.urlopen(url, timeout=2)
        if req.getcode() == 200:
            print("[SUCCESS] Chrome CDP port 9222 is ONLINE & DETACHED!")
            print(req.read().decode())
            break
    except Exception as e:
        print(f"Waiting... ({e})")
