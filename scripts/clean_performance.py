import pandas as pd

df = pd.read_csv(
    "data/raw/07_scheme_performance.csv"
)

return_cols = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct"
]

for col in return_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

anomalies = df[
    (df["expense_ratio_pct"] < 0.1)
    |
    (df["expense_ratio_pct"] > 2.5)
]

print(
    "Expense Ratio Anomalies:",
    len(anomalies)
)

df.to_csv(
    "data/processed/07_scheme_performance_clean.csv",
    index=False
)