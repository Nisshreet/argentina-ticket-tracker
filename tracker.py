import os
import csv
from datetime import datetime
from config import TARGET_PRICE, URLS
from telegram_notification import send_telegram
from sites.generic_site import get_lowest_price

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
prices = {}

os.makedirs("data", exist_ok=True)
csv_path = "data/price_history.csv"

if not os.path.isfile(csv_path):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "site", "price"])

for site, url in URLS.items():
    if "PASTE_" in url:
        print(f"{site}: skipped, no link yet")
        prices[site] = None
        continue

    lowest = get_lowest_price(url)
    prices[site] = lowest
    print(f"{site}: {lowest}")

    if lowest:
        with open(csv_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now, site, lowest])

valid_prices = {site: price for site, price in prices.items() if price is not None}

if valid_prices:
    cheapest_site = min(valid_prices, key=valid_prices.get)
    cheapest_price = valid_prices[cheapest_site]

    print("Cheapest:", cheapest_site, cheapest_price)

if cheapest_price <= TARGET_PRICE:
    message = (
        "🚨 PRICE ALERT 🚨\n\n"
        f"Argentina vs Jordan\n\n"
        f"Cheapest Price: ${cheapest_price}\n"
        f"Website: {cheapest_site}\n"
        f"Target: ${TARGET_PRICE}"
    )

    send_telegram(message)
    print("Price alert sent.")
else:
    print("No alert.")
