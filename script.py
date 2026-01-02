import requests
import os 
import snowflake.connector
from dotenv import load_dotenv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# Snowflake connection parameters
POLYGON_API_KEY = "1H2tFMSVy1fDw8T_nWx6qTH_D8vFRF1Q"
SNOWFLAKE_ACCOUNT = "REHNTRQ-OUB66781"
SNOWFLAKE_USER = "HUNTJA1995"
SNOWFLAKE_PASSWORD = "xucbiv-qonSyj-sawbo3"
SNOWFLAKE_WAREHOUSE = "SNOWFLAKE_LEARNING_WAREHOUSE"
SNOWFLAKE_DATABASE = "JACOBHUNT"
SNOWFLAKE_SCHEMA = "public"
SNOWFLAKE_ROLE = "accountadmin"
LIMIT = 1000

url = f'https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
response = requests.get(url)
tickers = []

data = response.json()
for ticker in data['results']:
    tickers.append(ticker)

while 'next_url' in data:
    print('requesting next page', data['next_url'])
    response = requests.get(data['next_url'] + f'&apikey={POLYGON_API_KEY}')
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)

# Connect to Snowflake
print('Connecting to Snowflake...')
conn = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

cursor = conn.cursor()

# Create table if it doesn't exist
create_table_sql = """
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
    composite_figi: VARCHAR(20),
    share_class_figi: VARCHAR(20),
    last_updated_utc TIMESTAMP_NTZ,
    ds: DATE,
    inserted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
"""

cursor.execute(create_table_sql)
print('Table created or already exists')

# Clear existing data (optional - remove if you want to append)
# cursor.execute("TRUNCATE TABLE tickers")

# Insert tickers into Snowflake
print(f'Inserting {len(tickers)} tickers into Snowflake...')
insert_sql = """
INSERT INTO tickers (ticker, name, market, locale, primary_exchange, type, active, currency_name, cik, last_updated_utc)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Prepare data for batch insert
ticker_data = []
for ticker in tickers:
    ticker_data.append((
        ticker.get('ticker'),
        ticker.get('name'),
        ticker.get('market'),
        ticker.get('locale'),
        ticker.get('primary_exchange'),
        ticker.get('type'),
        ticker.get('active'),
        ticker.get('currency_name'),
        ticker.get('cik'),
        ticker.get('last_updated_utc')
    ))

# Batch insert for better performance
cursor.executemany(insert_sql, ticker_data)
conn.commit()
print(f'Successfully inserted {len(tickers)} tickers into Snowflake table')

cursor.close()
conn.close()
print('Connection closed')