import pandas as pd

df = pd.read_csv(
    "data/raw/08_investor_transactions.csv"
)

df["transaction_type"] = (
    df["transaction_type"]
      .str.strip()
      .str.title()
)

valid_types = [
    "Sip",
    "Lumpsum",
    "Redemption"
]

df = df[
    df["transaction_type"].isin(valid_types)
]

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)

df = df[df["amount_inr"] > 0]

valid_kyc = [
    "Verified",
    "Pending"
]

df = df[
    df["kyc_status"].isin(valid_kyc)
]

df.to_csv(
    "data/processed/08_investor_transactions_clean.csv",
    index=False
)

print("Rows:", len(df))