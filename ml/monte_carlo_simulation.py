from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"
CHART_DIR = BASE_DIR / "reports" / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

print("Loading NAV data...")

nav = pd.read_csv(DATA_DIR / "02_nav_history_clean.csv")
fund_master = pd.read_csv(DATA_DIR / "01_fund_master_clean.csv")

nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])

# Select one key fund
selected_code = nav["amfi_code"].iloc[0]

fund_name = fund_master.loc[
    fund_master["amfi_code"] == selected_code,
    "scheme_name"
].iloc[0]

fund_nav = nav[nav["amfi_code"] == selected_code].copy()
fund_nav["daily_return"] = fund_nav["nav"].pct_change()

returns = fund_nav["daily_return"].dropna()

latest_nav = fund_nav["nav"].iloc[-1]
mean_return = returns.mean()
volatility = returns.std()

print(f"Selected Fund: {fund_name}")
print(f"Latest NAV: {latest_nav:.2f}")
print(f"Mean Daily Return: {mean_return:.6f}")
print(f"Daily Volatility: {volatility:.6f}")

# Monte Carlo settings
simulations = 1000
trading_days = 252 * 5   # 5 years

simulation_results = np.zeros((trading_days, simulations))

for sim in range(simulations):
    prices = [latest_nav]

    for day in range(1, trading_days):
        random_return = np.random.normal(mean_return, volatility)
        next_price = prices[-1] * (1 + random_return)
        prices.append(next_price)

    simulation_results[:, sim] = prices

simulation_df = pd.DataFrame(simulation_results)

summary = pd.DataFrame({
    "day": range(trading_days),
    "mean_nav": simulation_df.mean(axis=1),
    "p5_nav": simulation_df.quantile(0.05, axis=1),
    "p95_nav": simulation_df.quantile(0.95, axis=1)
})

summary.to_csv(
    DATA_DIR / "monte_carlo_results.csv",
    index=False
)

plt.figure(figsize=(12, 6))

for i in range(50):
    plt.plot(simulation_df.iloc[:, i], alpha=0.15)

plt.plot(summary["mean_nav"], linewidth=3, label="Mean Projection")
plt.plot(summary["p5_nav"], linestyle="--", label="5th Percentile")
plt.plot(summary["p95_nav"], linestyle="--", label="95th Percentile")

plt.title(f"Monte Carlo 5-Year NAV Projection\n{fund_name}")
plt.xlabel("Trading Days")
plt.ylabel("Projected NAV")
plt.legend()
plt.tight_layout()

chart_path = CHART_DIR / "monte_carlo_simulation.png"
plt.savefig(chart_path)
plt.close()

print("Monte Carlo simulation completed.")
print("Saved:")
print(DATA_DIR / "monte_carlo_results.csv")
print(chart_path)