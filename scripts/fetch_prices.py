"""
fetch_prices.py

This script fetches real-time cryptocurrency prices from the CoinGecko API,
logs the data into a CSV file, and writes process logs to both the console and a log file.

Environment Variables Required:
- API_BASE_URL: Base URL of the CoinGecko API (e.g., https://api.coingecko.com/api/v3)
- CRYPTOCURRENCIES: Comma-separated list of cryptocurrency IDs (e.g., bitcoin,ethereum)
"""


import requests
import datetime
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enforce required environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
if not API_BASE_URL:
    raise ValueError("Missing required environment variable: API_BASE_URL")

CRYPTOCURRENCIES = os.getenv("CRYPTOCURRENCIES")
if not CRYPTOCURRENCIES:
    raise ValueError("Missing required environment variable: CRYPTOCURRENCIES")

cryptos = CRYPTOCURRENCIES.split(',')

# Setup logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/fetch_prices.log"),
        logging.StreamHandler()
    ]
)

try:
    url = f"{API_BASE_URL}/simple/price"
    params = {'ids': ','.join(cryptos), 'vs_currencies': 'usd'}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("data", exist_ok=True)
    with open("data/prices.csv", "a") as f:
        for crypto in cryptos:
            price = data[crypto]['usd']
            f.write(f"{now},{crypto.upper()},{price}\n")

    logging.info(f"Fetched and logged prices for: {', '.join(cryptos)}")

except Exception as e:
    logging.error(f"Error fetching prices: {e}")
