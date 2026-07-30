import os
from playwright.sync_api import sync_playwright

def run_cuj(page):
    cwd = os.getcwd()
    page.goto(f"file://{cwd}/add_sub.html")
    page.wait_for_timeout(1000)

    # Click on the Pizza Game tab
    page.click("#tab-game")
    page.wait_for_timeout(1000)

    # Click on Scales game sub-tab
    page.click("#subtab-scales")
    page.wait_for_timeout(1000)

    # Interact with some scale buttons
    page.click("text=5 ק\"ג")
    page.wait_for_timeout(500)
    page.click("text=2 ק\"ג")
    page.wait_for_timeout(1000)

    # Take screenshot at the key moment
    page.screenshot(path="/home/jules/verification/screenshots/verification_add_sub.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
