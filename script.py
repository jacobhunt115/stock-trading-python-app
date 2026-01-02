import requests
import os 
import time
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# Config
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

def run_stock_job():
    print(f"--- Starting Data Fetch at {time.ctime()} ---")
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&limit=1000&apiKey={POLYGON_API_KEY}'
    tickers = []

    while url:
        response = requests.get(url)
        if response.status_code == 429:
            print("Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)
            continue
            
        data = response.json()
        if 'results' in data:
            tickers.extend(data['results'])
            print(f"Collected {len(tickers)} tickers...")
        
        next_url = data.get('next_url')
        if next_url:
            url = f"{next_url}&apiKey={POLYGON_API_KEY}"
            time.sleep(12) # Essential for free tier
        else:
            url = None

    if tickers:
        _save_to_snowflake(tickers)

def _save_to_snowflake(ticker_data):
    print("Connecting to Snowflake...")
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        role=SNOWFLAKE_ROLE
    )
    cursor = conn.cursor()

    # Fixing the 'No active warehouse' error
    cursor.execute(f"USE WAREHOUSE {SNOWFLAKE_WAREHOUSE}")
    cursor.execute(f"USE DATABASE {SNOWFLAKE_DATABASE}")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickers (
        ticker VARCHAR(50),
        name VARCHAR(500),
        market VARCHAR(50),
        locale VARCHAR(10),
        primary_exchange VARCHAR(20),
        type VARCHAR(20),
        active BOOLEAN,
        currency_name VARCHAR(10),
        cik VARCHAR(20),
        composite_figi VARCHAR(20),
        share_class_figi VARCHAR(20),
        last_updated_utc TIMESTAMP_NTZ,
        inserted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
    )
    """)

    insert_sql = """
    INSERT INTO tickers (ticker, name, market, locale, primary_exchange, type, active, currency_name, cik, composite_figi, share_class_figi, last_updated_utc)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    batch_data = [(
        t.get('ticker'), t.get('name'), t.get('market'), t.get('locale'),
        t.get('primary_exchange'), t.get('type'), t.get('active'),
        t.get('currency_name'), t.get('cik'), t.get('composite_figi'),
        t.get('share_class_figi'), t.get('last_updated_utc')
    ) for t in ticker_data]

    cursor.executemany(insert_sql, batch_data)
    conn.commit()
    cursor.close()
    conn.close()
    print("Job Complete. Data loaded to Snowflake.")

# THIS IS THE START BUTTON:
if __name__ == "__main__":
    run_stock_job()