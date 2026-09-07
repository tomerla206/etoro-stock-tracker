import os
import glob
import subprocess
import time
import urllib.request

profile_dir = os.path.expanduser(r"~\.chrome_debug_profile")

# Clean singleton lock files if any
for lock_file in glob.glob(os.path.join(profile_dir, "Singleton*")):
    try:
        os.remove(lock_file)
        print(f"Removed stale lock: {lock_file}")
    except Exception:
        pass

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

print(f"Launching Chrome with profile: {profile_dir}")
cmd = f'"{chrome_path}" --remote-debugging-port=9222 --user-data-dir="{profile_dir}" https://www.etoro.com/home'

# Launch via os.system / subprocess detached
subprocess.Popen(cmd, shell=True)

time.sleep(2)
try:
    url = "http://localhost:9222/json/version"
    req = urllib.request.urlopen(url, timeout=3)
    print("[SUCCESS] Connected to CDP on 9222!")
    print(req.read().decode())
except Exception as e:
    print(f"CDP check: {e}")
