import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

print("Attaching Selenium to Chrome on 127.0.0.1:9222 ...")
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(options=options)
    print("[SUCCESS] Selenium attached!")
    print("Current URL:", driver.current_url)
    print("Current Title:", driver.title)
except Exception as e:
    print(f"[!] Attachment failed: {e}")
