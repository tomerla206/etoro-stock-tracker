import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = os.path.abspath(".etoro_session")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        viewport={"width": 1280, "height": 800}
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://www.etoro.com/markets/rcmt/research", wait_until="domcontentloaded")
    time.sleep(5)
    
    text = page.inner_text("body")
    print("=== PAGE BODY TEXT SAMPLE ===")
    print(text[:1000])
    print("=============================")
    
    context.close()
