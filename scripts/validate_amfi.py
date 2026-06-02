import pandas as pd

master = pd.read_csv("data/raw/01_fund_master.csv")
history = pd.read_csv("data/raw/02_nav_history.csv")

master_codes = set(master["amfi_code"])
history_codes = set(history["amfi_code"])

missing_codes = master_codes - history_codes

print("Total fund master codes:", len(master_codes))
print("Total NAV history codes:", len(history_codes))
print("Missing codes:", len(missing_codes))

if missing_codes:
    print(missing_codes)
else:
    print("All AMFI codes validated successfully.")