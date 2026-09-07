import time
from playwright.sync_api import sync_playwright

print("Launching Playwright Chromium...")
with sync_playwright() as p:
    # Launch persistent context or browser
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.etoro.com/home")
    print("Page title:", page.title())
    time.sleep(3)
    browser.close()
print("Playwright test completed successfully!")
