import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_lowest_price(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        html = response.text

        matches = re.findall(r'\$([0-9,]+)', html)

        prices = []
        for match in matches:
            price = int(match.replace(",", ""))

            # Ignore suspicious low numbers for now
            if 1800 <= price <= 10000:
                prices.append(price)

        if not prices:
            return None

        return min(prices)

    except Exception as e:
        print("Error:", e)
        return None