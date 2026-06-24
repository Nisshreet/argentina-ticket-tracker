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
        with open("data/price_history.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now, site, lowest])

valid_prices = {site: price for site, price in prices.items() if price is not None}

if valid_prices:
    cheapest_site = min(valid_prices, key=valid_prices.get)
    cheapest_price = valid_prices[cheapest_site]

    print("Cheapest:", cheapest_site, cheapest_price)

message = (
    "📊 Hourly Ticket Update\n\n"
    "Argentina vs Jordan\n\n"
    f"Cheapest Price: ${cheapest_price}\n"
    f"Cheapest Website: {cheapest_site}\n"
    f"Target: ${TARGET_PRICE}\n\n"
    "All Websites:\n"
)

for site, price in prices.items():
    url = URLS.get(site, "")

    if price is None:
        message += f"\n❌ {site}: Not available\n{url}\n"
    else:
        message += f"\n✅ {site}: ${price}\n{url}\n"

send_telegram(message)
print("Telegram update sent.")
