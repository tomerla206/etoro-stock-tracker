import os
import glob
import subprocess
import time
import urllib.request

profile_dir = os.path.expanduser(r"~\.chrome_debug_profile")

# Clean singleton lock files
for lock_file in glob.glob(os.path.join(profile_dir, "Singleton*")):
    try:
        os.remove(lock_file)
    except Exception:
        pass

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Launch with DETACHED_PROCESS flag (0x00000008) so it survives parent exit
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

cmd = [
    chrome_path,
    f"--user-data-dir={profile_dir}",
    "--remote-debugging-port=9222",
    "https://www.etoro.com/home"
]

subprocess.Popen(
    cmd,
    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
    close_fds=True
)

print("Chrome launched as fully detached process!")
time.sleep(2)
try:
    url = "http://localhost:9222/json/version"
    req = urllib.request.urlopen(url, timeout=3)
    print("[SUCCESS] CDP port 9222 is ONLINE & STABLE!")
    print(req.read().decode())
except Exception as e:
    print(f"CDP check: {e}")
