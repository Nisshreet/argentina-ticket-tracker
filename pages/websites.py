import streamlit as st
import pandas as pd

DATA_FILE = "data/price_history.csv"

st.title("🌐 Websites Being Monitored")

df = pd.read_csv(DATA_FILE)

sites = [
    "StubHub",
    "TickPick",
    "Ticombo",
    "FIFA Marketplace",
    "SeatGeek",
    "Vivid Seats"
]

rows = []

for site in sites:
    site_data = df[df["site"] == site]

    if len(site_data) > 0:
        latest_price = int(site_data.iloc[-1]["price"])
        rows.append({
            "Website": site,
            "Status": "Live",
            "Price": f"${latest_price}"
        })
    else:
        rows.append({
            "Website": site,
            "Status": "Needs advanced scraper",
            "Price": "--"
        })

st.dataframe(pd.DataFrame(rows), use_container_width=True)