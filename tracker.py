import os
import csv
from datetime import datetime
from config import TARGET_PRICE, URLS
from telegram_notification import send_telegram
from sites.generic_site import get_lowest_price

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

prices = {}

for site, url in URLS.items():
    if "PASTE_" in url:
        print(f"{site}: skipped, no link yet")
        continue

    lowest = get_lowest_price(url)
    prices[site] = lowest

    print(f"{site}: {lowest}")

    if lowest:
        os.makedirs("data", exist_ok=True)

        if not os.path.exists("data/price_history.csv"):
            with open("data/price_history.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "site", "price"])

        with open("data/price_history.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now, site, lowest])

valid_prices = {site: price for site, price in prices.items() if price is not None}

if valid_prices:
    cheapest_site = min(valid_prices, key=valid_prices.get)
    cheapest_price = valid_prices[cheapest_site]

    print("Cheapest:", cheapest_site, cheapest_price)

    if cheapest_price <= TARGET_PRICE:
        message = f"""🚨 Argentina Ticket Alert

🇦🇷 Argentina vs Jordan

💰 Cheapest Price: ${cheapest_price}
🌐 Website: {cheapest_site}
🎯 Target: ${TARGET_PRICE}

All prices:
"""

        for site, price in valid_prices.items():
            message += f"{site}: ${price}\n"

        send_telegram(message)
    else:
        print("No alert.")
else:
    print("No valid prices found.")
