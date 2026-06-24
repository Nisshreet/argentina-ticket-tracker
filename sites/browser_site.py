from playwright.sync_api import sync_playwright
import re

def get_visible_lowest_price(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)

            text = page.locator("body").inner_text()

            browser.close()

        matches = re.findall(r'\$([0-9,]+)', text)

        prices = []
        for match in matches:
            price = int(match.replace(",", ""))

            if 100 <= price <= 10000:
                prices.append(price)

        if not prices:
            return None

        return min(prices)

    except Exception as e:
        print("Browser scraper error:", e)
        return None