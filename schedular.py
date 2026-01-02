import schedule
import time
from script import run_stock_job 
from datetime import datetime

def basic_job():
    print('Heartbeat: Scheduler is running at', datetime.now())

# Log a heartbeat every minute
schedule.every().minute.do(basic_job)

# Run the stock job every 30 minutes to avoid overlapping rate limits
schedule.every(30).minutes.do(run_stock_job)    

print("Scheduler started. Waiting for first run...")
while True:
    schedule.run_pending()
    time.sleep(1)