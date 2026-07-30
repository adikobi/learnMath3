import os
from playwright.sync_api import sync_playwright

def run_cuj(page):
    # Absolute filepath access as per memory
    cwd = os.getcwd()
    page.goto(f"file://{cwd}/shever.html")
    page.wait_for_timeout(1000)

    # Click on the Pizza Game tab
    page.click("#tab-game")
    page.wait_for_timeout(1000)

    # Click on Cashier game sub-tab
    page.click("#subtab-cashier")
    page.wait_for_timeout(1000)

    # Interact with some cashier elements (add 10, 1, 0.1)
    page.click("text=שטר ₪10")
    page.wait_for_timeout(500)
    page.click("text=₪1")
    page.wait_for_timeout(500)
    page.click("text=10 אג׳")
    page.wait_for_timeout(1000)

    # Take screenshot at the key moment
    page.screenshot(path="/home/jules/verification/screenshots/verification_shever.png")
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
