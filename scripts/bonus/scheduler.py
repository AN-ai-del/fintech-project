import os
import time
from datetime import datetime

print("Scheduler started...")

while True:
    now = datetime.now()

    # Run weekdays at 8 PM
    if now.weekday() < 5 and now.hour == 20 and now.minute == 0:
        print("Running ETL pipeline...")

        os.system("py scripts/live_nav_fetch.py")
        os.system("py scripts/load_sqlite.py")

        print("ETL completed successfully")

        time.sleep(60)

    time.sleep(30)