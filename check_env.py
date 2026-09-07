import sys

packages = ["playwright", "selenium", "requests", "bs4", "websocket"]
for pkg in packages:
    try:
        __import__(pkg)
        print(f"[+] {pkg}: INSTALLED")
    except ImportError:
        print(f"[-] {pkg}: NOT installed")
