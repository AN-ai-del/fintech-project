from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
SCRIPTS_DIR = BASE_DIR / "scripts"

CHARTS_DIR.mkdir(parents=True, exist_ok=True)
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)

print("Loading datasets...")

nav = pd.read_csv(DATA_DIR / "02_nav_history_clean.csv")
fund_master = pd.read_csv(DATA_DIR / "01_fund_master_clean.csv")
performance = pd.read_csv(DATA_DIR / "07_scheme_performance_clean.csv")
transactions = pd.read_csv(DATA_DIR / "08_investor_transactions_clean.csv")
holdings = pd.read_csv(DATA_DIR / "09_portfolio_holdings_clean.csv")

nav["date"] = pd.to_datetime(nav["date"])
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])

print("Datasets loaded successfully.")

# ==================================================
# 1. DAILY RETURNS
# ==================================================

print("Computing daily returns...")

nav = nav.sort_values(["amfi_code", "date"])
nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()

# ==================================================
# 2. HISTORICAL VAR AND CVAR
# ==================================================

print("Computing VaR and CVaR...")

var_results = []

for code in nav["amfi_code"].unique():
    temp = nav[nav["amfi_code"] == code].copy()
    returns = temp["daily_return"].dropna()

    if len(returns) == 0:
        continue

    var_95 = np.percentile(returns, 5)
    cvar_95 = returns[returns <= var_95].mean()

    var_results.append(
        {
            "amfi_code": code,
            "var_95": var_95,
            "cvar_95": cvar_95,
            "worst_daily_return": returns.min(),
            "avg_daily_return": returns.mean(),
            "daily_volatility": returns.std()
        }
    )

var_cvar_report = pd.DataFrame(var_results)

var_cvar_report = var_cvar_report.merge(
    fund_master[
        [
            "amfi_code",
            "scheme_name",
            "fund_house",
            "category",
            "sub_category",
            "risk_category"
        ]
    ],
    on="amfi_code",
    how="left"
)

var_cvar_report.to_csv(
    DATA_DIR / "var_cvar_report.csv",
    index=False
)

print("Saved var_cvar_report.csv")

# ==================================================
# 3. ROLLING 90-DAY SHARPE
# ==================================================

print("Computing rolling 90-day Sharpe...")

key_funds = nav["amfi_code"].drop_duplicates().head(5).tolist()

plt.figure(figsize=(14, 7))

for code in key_funds:
    temp = nav[nav["amfi_code"] == code].copy()
    temp = temp.sort_values("date")

    temp["rolling_sharpe_90d"] = (
        temp["daily_return"].rolling(90).mean()
        / temp["daily_return"].rolling(90).std()
    ) * np.sqrt(252)

    plt.plot(
        temp["date"],
        temp["rolling_sharpe_90d"],
        label=str(code)
    )

plt.title("Rolling 90-Day Sharpe Ratio for 5 Key Funds")
plt.xlabel("Date")
plt.ylabel("Rolling Sharpe Ratio")
plt.legend(title="AMFI Code")
plt.tight_layout()

rolling_chart_path = CHARTS_DIR / "rolling_sharpe_chart.png"
plt.savefig(rolling_chart_path)
plt.close()

print("Saved rolling_sharpe_chart.png")

# ==================================================
# 4. INVESTOR COHORT ANALYSIS
# ==================================================

print("Creating investor cohort analysis...")

first_txn = (
    transactions
    .groupby("investor_id")["transaction_date"]
    .min()
    .reset_index()
)

first_txn["cohort_year"] = first_txn["transaction_date"].dt.year

transactions = transactions.merge(
    first_txn[["investor_id", "cohort_year"]],
    on="investor_id",
    how="left"
)

sip_txns = transactions[
    transactions["transaction_type"].str.upper() == "SIP"
].copy()

avg_sip = (
    sip_txns
    .groupby("cohort_year")["amount_inr"]
    .mean()
    .reset_index()
    .rename(columns={"amount_inr": "avg_sip_amount"})
)

total_invested = (
    transactions
    .groupby("cohort_year")["amount_inr"]
    .sum()
    .reset_index()
    .rename(columns={"amount_inr": "total_invested"})
)

top_fund_pref = (
    transactions
    .groupby(["cohort_year", "amfi_code"])["amount_inr"]
    .sum()
    .reset_index()
)

top_fund_pref = top_fund_pref.sort_values(
    ["cohort_year", "amount_inr"],
    ascending=[True, False]
)

top_fund_pref = top_fund_pref.drop_duplicates("cohort_year")

top_fund_pref = top_fund_pref.rename(
    columns={
        "amfi_code": "top_preferred_amfi_code",
        "amount_inr": "top_fund_investment"
    }
)

cohort_report = (
    avg_sip
    .merge(total_invested, on="cohort_year", how="outer")
    .merge(top_fund_pref, on="cohort_year", how="outer")
)

cohort_report.to_csv(
    DATA_DIR / "investor_cohort_analysis.csv",
    index=False
)

print("Saved investor_cohort_analysis.csv")

# ==================================================
# 5. SIP CONTINUITY ANALYSIS
# ==================================================

print("Creating SIP continuity analysis...")

sip_txns = sip_txns.sort_values(["investor_id", "transaction_date"])

sip_txns["previous_sip_date"] = (
    sip_txns
    .groupby("investor_id")["transaction_date"]
    .shift(1)
)

sip_txns["gap_days"] = (
    sip_txns["transaction_date"]
    - sip_txns["previous_sip_date"]
).dt.days

sip_count = (
    sip_txns
    .groupby("investor_id")
    .size()
    .reset_index(name="sip_transaction_count")
)

avg_gap = (
    sip_txns
    .groupby("investor_id")["gap_days"]
    .mean()
    .reset_index(name="avg_gap_days")
)

sip_continuity = sip_count.merge(
    avg_gap,
    on="investor_id",
    how="left"
)

sip_continuity = sip_continuity[
    sip_continuity["sip_transaction_count"] >= 6
].copy()

sip_continuity["risk_flag"] = np.where(
    sip_continuity["avg_gap_days"] > 35,
    "At-Risk",
    "Regular"
)

sip_continuity.to_csv(
    DATA_DIR / "sip_continuity_report.csv",
    index=False
)

print("Saved sip_continuity_report.csv")

# ==================================================
# 6. SIMPLE FUND RECOMMENDER
# ==================================================

print("Creating recommender output...")

recommendation_base = performance.copy()

if "risk_grade" in recommendation_base.columns:
    risk_col = "risk_grade"
else:
    risk_col = "risk_category"

recommendation_base = recommendation_base.sort_values(
    "sharpe_ratio",
    ascending=False
)

recommender_results = []

for risk in ["Low", "Moderate", "High", "Very High"]:
    temp = recommendation_base[
        recommendation_base[risk_col].str.lower() == risk.lower()
    ].copy()

    top3 = temp.head(3)

    for _, row in top3.iterrows():
        recommender_results.append(
            {
                "risk_appetite": risk,
                "amfi_code": row["amfi_code"],
                "scheme_name": row["scheme_name"],
                "fund_house": row["fund_house"],
                "category": row["category"],
                "sharpe_ratio": row["sharpe_ratio"],
                "return_3yr_pct": row["return_3yr_pct"],
                "risk_grade": row[risk_col]
            }
        )

recommender_output = pd.DataFrame(recommender_results)

recommender_output.to_csv(
    DATA_DIR / "fund_recommendations.csv",
    index=False
)

print("Saved fund_recommendations.csv")

# ==================================================
# 7. SECTOR HHI CONCENTRATION
# ==================================================

print("Computing Sector HHI concentration...")

sector_weights = (
    holdings
    .groupby(["amfi_code", "sector"])["weight_pct"]
    .sum()
    .reset_index()
)

sector_weights["weight_decimal"] = sector_weights["weight_pct"] / 100

sector_weights["weight_squared"] = (
    sector_weights["weight_decimal"] ** 2
)

hhi_report = (
    sector_weights
    .groupby("amfi_code")["weight_squared"]
    .sum()
    .reset_index()
    .rename(columns={"weight_squared": "sector_hhi"})
)

hhi_report = hhi_report.merge(
    fund_master[
        [
            "amfi_code",
            "scheme_name",
            "fund_house",
            "category",
            "sub_category"
        ]
    ],
    on="amfi_code",
    how="left"
)

hhi_report = hhi_report.sort_values(
    "sector_hhi",
    ascending=False
)

hhi_report.to_csv(
    DATA_DIR / "sector_hhi_report.csv",
    index=False
)

print("Saved sector_hhi_report.csv")

# ==================================================
# 8. CREATE ADVANCED ANALYTICS NOTEBOOK
# ==================================================

print("Creating Advanced_Analytics.ipynb...")

try:
    import nbformat as nbf

    notebook = nbf.v4.new_notebook()

    notebook.cells = [
        nbf.v4.new_markdown_cell(
            "# Advanced Analytics + Risk Metrics\n\n"
            "This notebook summarizes Day 6 advanced analytics for the Mutual Fund Analytics Capstone Project."
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Historical VaR and CVaR\n\n"
            "Historical VaR at 95% confidence was calculated using the 5th percentile of daily returns. "
            "CVaR was calculated as the average of returns below the VaR threshold."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "var_cvar = pd.read_csv('../data/processed/var_cvar_report.csv')\n"
            "var_cvar.sort_values('var_95').head(10)"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Rolling 90-Day Sharpe Ratio\n\n"
            "Rolling Sharpe Ratio tracks the changing risk-adjusted performance of selected funds over time."
        ),
        nbf.v4.new_code_cell(
            "from IPython.display import Image\n"
            "Image(filename='../reports/charts/rolling_sharpe_chart.png')"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Investor Cohort Analysis\n\n"
            "Investors were grouped by the year of their first transaction to analyze cohort-level behavior."
        ),
        nbf.v4.new_code_cell(
            "cohort = pd.read_csv('../data/processed/investor_cohort_analysis.csv')\n"
            "cohort"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. SIP Continuity Analysis\n\n"
            "Investors with 6 or more SIP transactions were analyzed for average gap between SIP dates. "
            "Investors with gaps greater than 35 days were flagged as at-risk."
        ),
        nbf.v4.new_code_cell(
            "sip_continuity = pd.read_csv('../data/processed/sip_continuity_report.csv')\n"
            "sip_continuity['risk_flag'].value_counts()"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. Fund Recommender\n\n"
            "A simple rule-based recommender was created using risk appetite and Sharpe Ratio ranking."
        ),
        nbf.v4.new_code_cell(
            "recommendations = pd.read_csv('../data/processed/fund_recommendations.csv')\n"
            "recommendations"
        ),
        nbf.v4.new_markdown_cell(
            "## 6. Sector HHI Concentration\n\n"
            "Sector concentration was measured using HHI = sum of squared sector weights."
        ),
        nbf.v4.new_code_cell(
            "hhi = pd.read_csv('../data/processed/sector_hhi_report.csv')\n"
            "hhi.head(10)"
        ),
        nbf.v4.new_markdown_cell(
            "## 7. Advanced Insights\n\n"
            "1. Funds with the most negative VaR values have the highest downside risk exposure.\n"
            "2. CVaR gives a stricter view of tail losses compared to VaR.\n"
            "3. Rolling Sharpe Ratio helps identify periods of unstable risk-adjusted performance.\n"
            "4. SIP continuity analysis identifies investors who may be at risk of discontinuing systematic investments.\n"
            "5. Sector HHI highlights funds with concentrated portfolio exposure."
        )
    ]

    output_path = NOTEBOOKS_DIR / "Advanced_Analytics.ipynb"

    with open(output_path, "w", encoding="utf-8") as f:
        nbf.write(notebook, f)

    print("Saved Advanced_Analytics.ipynb")

except Exception as e:
    print("Could not create notebook automatically.")
    print("Reason:", e)

print("Day 6 advanced analytics completed successfully.")