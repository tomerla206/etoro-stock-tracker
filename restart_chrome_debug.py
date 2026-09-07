import os
import subprocess
import sys
import time
import urllib.request

def kill_chrome():
    print("Closing active Chrome processes...")
    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
    time.sleep(2)

def launch_debug_chrome():
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
        print("Chrome executable not found!")
        return False

    cmd = [chrome_path, "--remote-debugging-port=9222", "https://www.etoro.com/home"]
    print(f"Starting Chrome from: {chrome_path} with --remote-debugging-port=9222...")
    subprocess.Popen(cmd)
    
    # Wait for CDP to respond
    for _ in range(10):
        time.sleep(1)
        try:
            url = "http://localhost:9222/json/version"
            req = urllib.request.urlopen(url, timeout=2)
            if req.getcode() == 200:
                print("\n[SUCCESS] Chrome is now running in Debugging mode on port 9222!")
                return True
        except Exception:
            pass
    print("\n[!] Could not connect to CDP port 9222.")
    return False

if __name__ == "__main__":
    kill_chrome()
    launch_debug_chrome()
