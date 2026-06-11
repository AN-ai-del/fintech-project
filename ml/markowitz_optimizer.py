from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "processed"
CHART_DIR = BASE_DIR / "reports" / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

print("Loading NAV history...")

nav = pd.read_csv(
    DATA_DIR / "02_nav_history_clean.csv"
)

nav["date"] = pd.to_datetime(nav["date"])

# Select first 5 funds

funds = nav["amfi_code"].unique()[:5]

print("Funds selected:")
print(funds)

pivot = nav[
    nav["amfi_code"].isin(funds)
].pivot(
    index="date",
    columns="amfi_code",
    values="nav"
)

returns = pivot.pct_change().dropna()

annual_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

num_portfolios = 5000

results = []

print("Generating portfolios...")

for _ in range(num_portfolios):

    weights = np.random.random(len(funds))
    weights = weights / np.sum(weights)

    portfolio_return = np.sum(
        annual_returns * weights
    )

    portfolio_volatility = np.sqrt(
        np.dot(
            weights.T,
            np.dot(cov_matrix, weights)
        )
    )

    sharpe_ratio = (
        portfolio_return /
        portfolio_volatility
    )

    row = {
        "return": portfolio_return,
        "risk": portfolio_volatility,
        "sharpe": sharpe_ratio
    }

    for i, fund in enumerate(funds):
        row[f"weight_{fund}"] = weights[i]

    results.append(row)

frontier = pd.DataFrame(results)

frontier.to_csv(
    DATA_DIR / "efficient_frontier_results.csv",
    index=False
)

print("efficient_frontier_results.csv saved")

best_portfolio = frontier.loc[
    frontier["sharpe"].idxmax()
]

print("\nBest Portfolio")
print(best_portfolio)

plt.figure(figsize=(12,7))

plt.scatter(
    frontier["risk"],
    frontier["return"],
    c=frontier["sharpe"],
    alpha=0.5
)

plt.colorbar(label="Sharpe Ratio")

plt.scatter(
    best_portfolio["risk"],
    best_portfolio["return"],
    marker="*",
    s=400,
    label="Best Sharpe Portfolio"
)

plt.xlabel("Risk (Volatility)")
plt.ylabel("Expected Return")

plt.title(
    "Markowitz Efficient Frontier"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    CHART_DIR / "efficient_frontier.png"
)

plt.close()

print("efficient_frontier.png saved")