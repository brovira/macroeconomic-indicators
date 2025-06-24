import os
import datetime as dt
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf
from fredapi import Fred


@st.cache_data
def load_yfinance_data(symbol: str, start: dt.date, end: dt.date) -> pd.Series:
    """Load adjusted close prices from yfinance."""
    data = yf.download(symbol, start=start, end=end, progress=False)
    if "Adj Close" in data:
        series = data["Adj Close"]
    else:
        series = data["Close"]
    series.index = pd.to_datetime(series.index)
    series.name = symbol
    return series


@st.cache_data
def load_fred_data(series_id: str, start: dt.date, end: dt.date, fred: Fred) -> pd.Series:
    """Fetch series data from the FRED API."""
    series = fred.get_series(series_id, observation_start=start, observation_end=end)
    series.index = pd.to_datetime(series.index)
    series.name = series_id
    return series


def main() -> None:
    st.set_page_config(page_title="Macroeconomic Indicators", layout="wide")
    st.title("Macroeconomic Indicators Dashboard")

    st.sidebar.write("## Date Range")
    today = dt.date.today()
    default_start = today.replace(year=today.year - 5)
    start_date = st.sidebar.date_input("Start", value=default_start)
    end_date = st.sidebar.date_input("End", value=today)

    fred_api_key = '8eaa91c32107a306db4ec5d8f097ca8d' """os.environ.get("FRED_API_KEY")"""
    if not fred_api_key:
        st.error("FRED_API_KEY environment variable not set. FRED data cannot be loaded.")
        return

    fred = Fred(api_key=fred_api_key)

    indicators = {
        "Bitcoin (BTC-USD)": ("yfinance", "BTC-USD"),
        "Gold (GC=F)": ("yfinance", "GC=F"),
        "Oil (CL=F)": ("yfinance", "CL=F"),
        "US 10Y Treasury Yield (TNX)": ("yfinance", "^TNX"),
        "M2 Money Stock": ("fred", "M2SL"),
        "Consumer Price Index": ("fred", "CPIAUCSL"),
    }

    tabs = st.tabs(list(indicators.keys()))

    for (name, (source, symbol)), tab in zip(indicators.items(), tabs):
        with tab:
            if source == "yfinance":
                series = load_yfinance_data(symbol, start_date, end_date)
            else:
                series = load_fred_data(symbol, start_date, end_date, fred)

            fig = px.line(series, title=name, labels={"value": name, "index": "Date"})
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(series.rename("Value"))


if __name__ == "__main__":
    main()
