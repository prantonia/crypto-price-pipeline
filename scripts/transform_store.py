"""
transform_store.py

This script reads the raw cryptocurrency prices from prices.csv,
transforms the data into a structured format, and stores it in a PostgreSQL database.

"""

import pandas as pd
import psycopg2
import os
import logging
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/transform_store.log"),
        logging.StreamHandler()  # prints to console
    ]
)


try:
    df = pd.read_csv("data/prices.csv", names=["timestamp", "currency", "price"])
    
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE")
    )

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            timestamp TIMESTAMP,
            currency TEXT,
            price NUMERIC
        );
    """)

    for _, row in df.iterrows():
        cursor.execute(
            'INSERT INTO prices (timestamp, currency, price) VALUES (%s, %s, %s)',
            (row['timestamp'], row['currency'], row['price'])
        )

    conn.commit()
    cursor.close()
    conn.close()

    # Clear CSV after storing
    open("data/prices.csv", "w").close()

    logging.info(f"Inserted {len(df)} rows into the database.")

except Exception as e:
    logging.error(f"Error transforming/storing data: {e}")