import json
import pandas as pd
from datetime import datetime

try:
    with open("data/live/sample_nav.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("sample_nav.json not found")
    exit()

print("Loading sample NAV data...")

nav_df = pd.DataFrame(data["data"])

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

filename = f"data/live/nav_{timestamp}.csv"

nav_df.to_csv(
    filename,
    index=False
)

print(f"Saved: {filename}")