import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

print("Testing Selenium ChromeDriver launcher...")
try:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    print("[SUCCESS] Chrome opened via Selenium!")
    driver.get("https://www.etoro.com/home")
    print("Page title:", driver.title)
    driver.quit()
except Exception as e:
    print(f"[!] Selenium launch failed: {e}")
