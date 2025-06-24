# Macroeconomic Indicators Dashboard

This repository provides a Streamlit application that visualizes several macroeconomic indicators using Plotly.

## Setup

1. Create a Python virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Obtain a FRED API key from [Federal Reserve Economic Data](https://fred.stlouisfed.org/) and set it as an environment variable:
   ```bash
   export FRED_API_KEY=your_api_key
   ```
4. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

The dashboard loads data for:
- Bitcoin (BTC-USD)
- Gold (GC=F)
- Oil (CL=F)
- US 10-Year Treasury Yield (TNX)
- M2 Money Stock (FRED series `M2SL`)
- Consumer Price Index (FRED series `CPIAUCSL`)
