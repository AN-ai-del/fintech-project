import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("Loading datasets...")

nav = pd.read_csv(
    "data/processed/02_nav_history_clean.csv"
)

scorecard = pd.read_csv(
    "data/processed/fund_scorecard.csv"
)

benchmark = pd.read_csv(
    "data/processed/10_benchmark_indices_clean.csv"
)

nav["date"] = pd.to_datetime(nav["date"])
benchmark["date"] = pd.to_datetime(benchmark["date"])

print("Selecting top 5 funds...")

top5 = (
    scorecard
    .sort_values(
        "fund_score",
        ascending=False
    )
    .head(5)
)

codes = top5["amfi_code"].tolist()

plt.figure(figsize=(14,8))

for code in codes:
    
    temp = nav[
        nav["amfi_code"] == code
    ].copy()
    
    temp = temp.sort_values("date")
    
    temp["growth"] = (
        temp["nav"] /
        temp["nav"].iloc[0]
    ) * 100
    
    plt.plot(
        temp["date"],
        temp["growth"],
        label=f"Fund {code}"
    )

for index_name in benchmark[
    "index_name"
].unique()[:2]:
    
    temp = benchmark[
        benchmark["index_name"] == index_name
    ].copy()
    
    temp = temp.sort_values("date")
    
    temp["growth"] = (
        temp["close_value"] /
        temp["close_value"].iloc[0]
    ) * 100
    
    plt.plot(
        temp["date"],
        temp["growth"],
        linewidth=3,
        label=index_name
    )

plt.title(
    "Top 5 Funds vs Benchmarks"
)

plt.xlabel("Date")
plt.ylabel("Growth Index")

plt.legend()

plt.tight_layout()

plt.savefig(
    "reports/charts/benchmark_comparison.png"
)

plt.close()

print("benchmark_comparison.png saved")