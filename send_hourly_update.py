import pandas as pd
from config import URLS, TARGET_PRICE
from telegram_notification import send_telegram

DATA_FILE = "data/price_history.csv"

df = pd.read_csv(DATA_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"])

latest = df.sort_values("timestamp").groupby("site").tail(1)

cheapest_row = latest.loc[latest["price"].idxmin()]
cheapest_site = cheapest_row["site"]
cheapest_price = int(cheapest_row["price"])
last_updated = latest["timestamp"].max()

message = f"""📊 Hourly Ticket Update

🇦🇷 Argentina vs Jordan

💰 Cheapest: ${cheapest_price}
🌐 Website: {cheapest_site}
🎯 Target: ${TARGET_PRICE}
🕒 Last Updated: {last_updated}

All Websites:
"""

for site, url in URLS.items():
    site_data = latest[latest["site"] == site]

    if len(site_data) > 0:
        price = int(site_data.iloc[-1]["price"])
        message += f"\n✅ {site}: ${price}\n{url}\n"
    else:
        message += f"\n⚠️ {site}: No readable price yet\n{url}\n"

send_telegram(message)
print("Hourly Telegram update sent.")