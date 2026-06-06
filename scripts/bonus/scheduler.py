import schedule
import subprocess
import time


def fetch_nav():

    print("Running NAV fetch...")

    subprocess.run(
        [
            "py",
            "scripts/bonus/live_nav_fetch.py"
        ]
    )


schedule.every().monday.at("20:00").do(fetch_nav)
schedule.every().tuesday.at("20:00").do(fetch_nav)
schedule.every().wednesday.at("20:00").do(fetch_nav)
schedule.every().thursday.at("20:00").do(fetch_nav)
schedule.every().friday.at("20:00").do(fetch_nav)

print("Scheduler started")

while True:

    schedule.run_pending()

    time.sleep(60)