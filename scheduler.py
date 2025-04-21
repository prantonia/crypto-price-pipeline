"""
scheduler.py

This script schedules the automatic fetching and transformation of cryptocurrency prices
at a regular interval.


This script assumes:
- fetch_prices.py fetches current prices and appends to data/prices.csv
- transform_store.py loads data from CSV and inserts it into PostgreSQL
"""

import schedule
import time
import os
import logging

# Setup logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/scheduler.log"),
        logging.StreamHandler()  # prints to console
    ]
)

def run_pipeline():

    """
    Runs the fetch_prices and transform_store scripts sequentially.

    """
    logging.info("Running every 15 minutes pipeline...")
    try:
        os.system("python scripts/fetch_prices.py")
        os.system("python scripts/transform_store.py")
        logging.info("Pipeline run completed.")
    except Exception as e:
        logging.error(f"Error running pipeline: {e}")

#schedule.every().hour.at(":00").do(run_pipeline)

schedule.every(15).minutes.do(run_pipeline)


logging.info("Scheduler started. Waiting for the next scheduled run...")


while True:
        schedule.run_pending()
        time.sleep(1)


