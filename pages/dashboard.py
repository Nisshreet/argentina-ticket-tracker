import os
import streamlit as st
import pandas as pd

st.title("🏠 Dashboard")

DATA_FILE = "data/price_history.csv"

if not os.path.exists(DATA_FILE):
    st.warning("No price history yet. Run the tracker first.")
    st.stop()

df = pd.read_csv(DATA_FILE)

if df.empty:
    st.warning("No price data yet.")
    st.stop()

st.subheader("Latest Prices")

latest = df.sort_values("timestamp").groupby("site").tail(1)
st.dataframe(latest)

st.subheader("Price History")

df["timestamp"] = pd.to_datetime(df["timestamp"])
pivot = df.pivot_table(index="timestamp", columns="site", values="price")
st.line_chart(pivot)