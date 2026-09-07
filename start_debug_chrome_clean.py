import os
import subprocess
import time
import urllib.request

print("Closing all existing Chrome background tasks...")
subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
time.sleep(2)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

print("Starting main Chrome with --remote-debugging-port=9222 ...")
cmd = [chrome_path, "--remote-debugging-port=9222", "https://www.etoro.com/home"]

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

subprocess.Popen(
    cmd,
    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
    close_fds=True
)

for i in range(10):
    time.sleep(1)
    try:
        url = "http://localhost:9222/json/version"
        req = urllib.request.urlopen(url, timeout=2)
        if req.getcode() == 200:
            print("\n[SUCCESS!] Chrome is running on port 9222 with default user profile!")
            print(req.read().decode())
            break
    except Exception as e:
        print(f"Waiting for Chrome port 9222... ({i+1}/10)")
