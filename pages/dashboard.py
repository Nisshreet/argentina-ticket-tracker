import streamlit as st
import pandas as pd
import plotly.express as px
from config import TARGET_PRICE

DATA_FILE = "data/price_history.csv"

st.title("🏠 Dashboard")

df = pd.read_csv(DATA_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"])

latest_by_site = df.sort_values("timestamp").groupby("site").tail(1)
cheapest_row = latest_by_site.loc[latest_by_site["price"].idxmin()]

cheapest_price = int(cheapest_row["price"])
cheapest_site = cheapest_row["site"]

if cheapest_price <= TARGET_PRICE:
    recommendation = "BUY NOW"
else:
    recommendation = "WAIT"

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Cheapest Price", f"${cheapest_price}")
col2.metric("🌐 Cheapest Site", cheapest_site)
col3.metric("🎯 Target Price", f"${TARGET_PRICE}")
col4.metric("🤖 AI Recommendation", recommendation)

st.divider()

fig = px.line(
    df,
    x="timestamp",
    y="price",
    color="site",
    markers=True,
    title="Ticket Price Trend"
)

st.plotly_chart(fig, use_container_width=True)