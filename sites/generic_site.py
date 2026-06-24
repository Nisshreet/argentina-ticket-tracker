import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_lowest_price(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        html = response.text

        patterns = [
            r'\$([0-9,]+)',
            r'"price"\s*:\s*"?([0-9,]+)"?',
            r'"lowPrice"\s*:\s*"?([0-9,]+)"?',
            r'"minPrice"\s*:\s*"?([0-9,]+)"?',
        ]

        prices = []

        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                price = int(str(match).replace(",", ""))

                if 600 <= price <= 10000:
                    prices.append(price)

        if not prices:
            return None

        return min(prices)

    except Exception as e:
        print("Error:", e)
        return None