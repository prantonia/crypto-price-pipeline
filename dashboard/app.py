"""
app.py

Streamlit dashboard to visualize the latest cryptocurrency prices.

Features:
- Auto-refresh countdown
- Line charts for Bitcoin and Ethereum (last 10 entries)
- Data source: PostgreSQL database

"""


import streamlit as st
import time
import pandas as pd
from sqlalchemy import create_engine
import os
import altair as alt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("📈 Crypto Price Tracker")

st.markdown("""
This dashboard shows the latest **Bitcoin** and **Ethereum** prices stored in the database.  
The charts below auto-refresh every 15 minutes to show new entries collected by the pipeline.
""")

try:
    # Create SQLAlchemy database URL
    db_url = f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@" \
             f"{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
    
    # Create a database engine
    engine = create_engine(db_url)
    
    # Load full recent data
    raw_query = "SELECT * FROM prices ORDER BY timestamp DESC"
    raw_df = pd.read_sql(raw_query, engine)  # Use engine instead of connection
    engine.dispose()  # Dispose of the engine

    if not raw_df.empty:
        # Drop duplicate timestamps and currency, keeping the first occurrence
        df = raw_df.drop_duplicates(subset=["timestamp", "currency"]).head(20).reset_index(drop=True)

        st.subheader("📋 Last 20 Entries")
        st.dataframe(df)

        # Sort in chronological order for visualization
        df = df.sort_values(by="timestamp")

        # Split Bitcoin and Ethereum for charts (sort then take last 10 per currency)
        btc_df = df[df["currency"] == "BITCOIN"].sort_values(by="timestamp").tail(10).copy()
        eth_df = df[df["currency"] == "ETHEREUM"].sort_values(by="timestamp").tail(10).copy()

        # Create time labels for charts
        btc_df["time_label"] = btc_df["timestamp"].dt.strftime("%H:%M")
        eth_df["time_label"] = eth_df["timestamp"].dt.strftime("%H:%M")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("₿ Bitcoin Price Trend")
            if not btc_df.empty:
                chart_btc = alt.Chart(btc_df).mark_line(point=True).encode(
                    x=alt.X("timestamp:T", title="Time", axis=alt.Axis(format="%H:%M", labelAngle=0)),
                    y=alt.Y("price:Q", title="Price ($)", scale=alt.Scale(zero=False)),
                    tooltip=["timestamp:T", "price:Q"]
                ).properties(height=300)
                st.altair_chart(chart_btc, use_container_width=True)

        with col2:
            st.subheader("Ξ Ethereum Price Trend")
            if not eth_df.empty:
                chart_eth = alt.Chart(eth_df).mark_line(point=True).encode(
                    x=alt.X("timestamp:T", title="Time", axis=alt.Axis(format="%H:%M", labelAngle=0)),
                    y=alt.Y("price:Q", title="Price ($)", scale=alt.Scale(zero=False)),
                    tooltip=["timestamp:T", "price:Q"]
                ).properties(height=300)
                st.altair_chart(chart_eth, use_container_width=True)

    else:
        st.warning("No data available in the database yet.")

except Exception as e:
    st.error(f"Database error: {e}")

# Set a refresh interval (in seconds)
refresh_interval = 900

# Streamlit placeholders
countdown_placeholder = st.sidebar.empty()
progress_bar = st.sidebar.empty()

# Countdown loop
for remaining in range(refresh_interval, 0, -1):
    countdown_placeholder.markdown(f"⏳ Refreshing in **{remaining}** seconds...")
    progress_bar.progress(remaining / refresh_interval)
    time.sleep(1)

# Trigger rerun when countdown finishes
st.rerun()