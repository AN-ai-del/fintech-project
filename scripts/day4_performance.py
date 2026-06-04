import pandas as pd
import numpy as np

print("Loading datasets...")

nav = pd.read_csv(
    "data/processed/02_nav_history_clean.csv"
)

nav["date"] = pd.to_datetime(
    nav["date"]
)

nav = nav.sort_values(
    ["amfi_code", "date"]
)

print("Rows:", len(nav))

# --------------------------
# DAILY RETURNS
# --------------------------

print("Computing daily returns...")

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
       .pct_change()
)

nav.to_csv(
    "data/processed/daily_returns.csv",
    index=False
)

print("daily_returns.csv saved")

# --------------------------
# CAGR
# --------------------------

print("Computing CAGR...")

cagr_results = []

for fund in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == fund
    ].sort_values("date")

    start_nav = temp["nav"].iloc[0]
    end_nav = temp["nav"].iloc[-1]

    years = (
        temp["date"].max()
        - temp["date"].min()
    ).days / 365

    cagr = (
        (end_nav / start_nav)
        ** (1 / years)
        - 1
    )

    cagr_results.append(
        [fund, cagr]
    )

cagr_df = pd.DataFrame(
    cagr_results,
    columns=[
        "amfi_code",
        "cagr"
    ]
)

cagr_df.to_csv(
    "data/processed/cagr.csv",
    index=False
)

print("cagr.csv saved")

# --------------------------
# SHARPE RATIO
# --------------------------

print("Computing Sharpe Ratios...")

rf = 0.065

sharpe_results = []

for fund in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == fund
    ]

    returns = temp["daily_return"].dropna()

    annual_return = (
        returns.mean() * 252
    )

    annual_volatility = (
        returns.std() * np.sqrt(252)
    )

    sharpe = (
        annual_return - rf
    ) / annual_volatility

    sharpe_results.append(
        [fund, sharpe]
    )

sharpe_df = pd.DataFrame(
    sharpe_results,
    columns=[
        "amfi_code",
        "sharpe_ratio"
    ]
)

sharpe_df.to_csv(
    "data/processed/sharpe_ratio.csv",
    index=False
)

print("sharpe_ratio.csv saved")


# --------------------------
# SORTINO RATIO
# --------------------------

print("Computing Sortino Ratios...")

sortino_results = []

for fund in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == fund
    ]

    returns = temp["daily_return"].dropna()

    downside = returns[
        returns < 0
    ]

    downside_std = (
        downside.std() * np.sqrt(252)
    )

    annual_return = (
        returns.mean() * 252
    )

    sortino = (
        annual_return - rf
    ) / downside_std

    sortino_results.append(
        [fund, sortino]
    )

sortino_df = pd.DataFrame(
    sortino_results,
    columns=[
        "amfi_code",
        "sortino_ratio"
    ]
)

sortino_df.to_csv(
    "data/processed/sortino_ratio.csv",
    index=False
)

print("sortino_ratio.csv saved")

from scipy.stats import linregress

print("Computing Alpha & Beta...")

benchmark = pd.read_csv(
    "data/processed/10_benchmark_indices_clean.csv"
)

benchmark["date"] = pd.to_datetime(
    benchmark["date"]
)

benchmark = benchmark.sort_values("date")

# Use first benchmark available
benchmark = benchmark[
    benchmark["index_name"]
    ==
    benchmark["index_name"].iloc[0]
]

benchmark["benchmark_return"] = (
    benchmark["close_value"].pct_change()
)

alpha_beta_results = []

for code in nav["amfi_code"].unique():

    fund = nav[
        nav["amfi_code"] == code
    ].copy()

    fund = fund.sort_values("date")

    fund["daily_return"] = (
        fund["nav"].pct_change()
    )

    merged = pd.merge(
        fund[["date", "daily_return"]],
        benchmark[["date", "benchmark_return"]],
        on="date",
        how="inner"
    )

    merged = merged.dropna()

    if len(merged) > 30:

        beta, alpha, r_value, p_value, std_err = linregress(
            merged["benchmark_return"],
            merged["daily_return"]
        )

        alpha_beta_results.append(
            [
                code,
                alpha * 252,
                beta
            ]
        )

alpha_beta_df = pd.DataFrame(
    alpha_beta_results,
    columns=[
        "amfi_code",
        "alpha",
        "beta"
    ]
)

alpha_beta_df.to_csv(
    "data/processed/alpha_beta.csv",
    index=False
)

print("alpha_beta.csv saved")

print("Computing Maximum Drawdown...")

drawdown_results = []

for code in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == code
    ].copy()

    temp = temp.sort_values("date")

    temp["running_max"] = (
        temp["nav"].cummax()
    )

    temp["drawdown"] = (
        temp["nav"] /
        temp["running_max"]
    ) - 1

    max_dd = temp["drawdown"].min()

    drawdown_results.append(
        [code, max_dd]
    )

drawdown_df = pd.DataFrame(
    drawdown_results,
    columns=[
        "amfi_code",
        "max_drawdown"
    ]
)

drawdown_df.to_csv(
    "data/processed/max_drawdown.csv",
    index=False
)

print("max_drawdown.csv saved")

print("Creating Fund Scorecard...")

scorecard = (
    cagr_df.merge(
        sharpe_df,
        on="amfi_code"
    )
    .merge(
        alpha_beta_df,
        on="amfi_code"
    )
    .merge(
        drawdown_df,
        on="amfi_code"
    )
)

scorecard["cagr_rank"] = (
    scorecard["cagr"]
    .rank(ascending=False)
)

scorecard["sharpe_rank"] = (
    scorecard["sharpe_ratio"]
    .rank(ascending=False)
)

scorecard["alpha_rank"] = (
    scorecard["alpha"]
    .rank(ascending=False)
)

scorecard["dd_rank"] = (
    scorecard["max_drawdown"]
    .rank(ascending=False)
)

scorecard["fund_score"] = (
    30 * (1 / scorecard["cagr_rank"])
    + 25 * (1 / scorecard["sharpe_rank"])
    + 20 * (1 / scorecard["alpha_rank"])
    + 10 * (1 / scorecard["dd_rank"])
)

scorecard = scorecard.sort_values(
    "fund_score",
    ascending=False
)

scorecard.to_csv(
    "data/processed/fund_scorecard.csv",
    index=False
)

print("fund_scorecard.csv saved")