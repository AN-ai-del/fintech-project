import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme()

# ==================================================
# CREATE OUTPUT FOLDER
# ==================================================

os.makedirs("reports/charts", exist_ok=True)

# ==================================================
# LOAD DATASETS
# ==================================================

print("Loading datasets...")

nav = pd.read_csv(
    "data/processed/02_nav_history_clean.csv"
)

sip = pd.read_csv(
    "data/processed/04_monthly_sip_inflows_clean.csv"
)

aum = pd.read_csv(
    "data/processed/03_aum_by_fund_house_clean.csv"
)

transactions = pd.read_csv(
    "data/processed/08_investor_transactions_clean.csv"
)

folios = pd.read_csv(
    "data/processed/06_industry_folio_count_clean.csv"
)

performance = pd.read_csv(
    "data/processed/07_scheme_performance_clean.csv"
)

holdings = pd.read_csv(
    "data/processed/09_portfolio_holdings_clean.csv"
)

category = pd.read_csv(
    "data/processed/05_category_inflows_clean.csv"
)

print("All datasets loaded successfully")

# ==================================================
# 1. NAV TREND
# ==================================================

print("Creating NAV trend chart...")

nav["date"] = pd.to_datetime(nav["date"])

plt.figure(figsize=(12, 6))

for code in nav["amfi_code"].unique()[:10]:
    temp = nav[nav["amfi_code"] == code]
    plt.plot(temp["date"], temp["nav"])

plt.title("NAV Trends")
plt.xlabel("Date")
plt.ylabel("NAV")

plt.savefig(
    "reports/charts/nav_trends.png"
)

plt.close()

# ==================================================
# 2. AUM GROWTH
# ==================================================

print("Creating AUM chart...")

aum["date"] = pd.to_datetime(aum["date"])
aum["year"] = aum["date"].dt.year

top_funds = (
    aum["fund_house"]
    .value_counts()
    .head(5)
    .index
)

aum_filtered = aum[
    aum["fund_house"].isin(top_funds)
]

plt.figure(figsize=(12, 6))

sns.barplot(
    data=aum_filtered,
    x="year",
    y="aum_lakh_crore",
    hue="fund_house"
)

plt.title("AUM Growth by Fund House")

plt.savefig(
    "reports/charts/aum_growth.png"
)

plt.close()

# ==================================================
# 3. SIP TREND
# ==================================================

print("Creating SIP chart...")

sip["month"] = pd.to_datetime(
    sip["month"]
)

plt.figure(figsize=(12, 6))

plt.plot(
    sip["month"],
    sip["sip_inflow_crore"]
)

plt.title("Monthly SIP Inflows")
plt.xlabel("Month")
plt.ylabel("Crore INR")

plt.savefig(
    "reports/charts/sip_trend.png"
)

plt.close()

# ==================================================
# 4. GENDER DISTRIBUTION
# ==================================================

print("Creating gender chart...")

gender_counts = (
    transactions["gender"]
    .value_counts()
)

plt.figure(figsize=(6, 6))

plt.pie(
    gender_counts,
    labels=gender_counts.index,
    autopct="%1.1f%%"
)

plt.title("Gender Distribution")

plt.savefig(
    "reports/charts/gender_distribution.png"
)

plt.close()

# ==================================================
# 5. AGE DISTRIBUTION
# ==================================================

print("Creating age chart...")

plt.figure(figsize=(8, 5))

transactions["age_group"] \
    .value_counts() \
    .plot(kind="bar")

plt.title("Age Group Distribution")

plt.savefig(
    "reports/charts/age_distribution.png"
)

plt.close()

# ==================================================
# 6. STATE TRANSACTIONS
# ==================================================

print("Creating state chart...")

state_data = (
    transactions
    .groupby("state")["amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

state_data.plot(
    kind="barh"
)

plt.title(
    "Top States by Transaction Amount"
)

plt.savefig(
    "reports/charts/state_transactions.png"
)

plt.close()

# ==================================================
# 7. CATEGORY HEATMAP
# ==================================================

print("Creating category heatmap...")

pivot_table = category.pivot(
    index="category",
    columns="month",
    values="net_inflow_crore"
)

plt.figure(figsize=(12, 8))

sns.heatmap(
    pivot_table
)

plt.title(
    "Category Inflow Heatmap"
)

plt.savefig(
    "reports/charts/category_heatmap.png"
)

plt.close()

# ==================================================
# 8. FOLIO GROWTH
# ==================================================

print("Creating folio growth chart...")

folios["month"] = pd.to_datetime(
    folios["month"]
)

plt.figure(figsize=(12, 6))

plt.plot(
    folios["month"],
    folios["total_folios_crore"]
)

plt.title(
    "Industry Folio Growth"
)

plt.savefig(
    "reports/charts/folio_growth.png"
)

plt.close()

# ==================================================
# 9. T30 VS B30
# ==================================================

print("Creating city tier chart...")

tier_counts = (
    transactions["city_tier"]
    .value_counts()
)

plt.figure(figsize=(6, 6))

plt.pie(
    tier_counts,
    labels=tier_counts.index,
    autopct="%1.1f%%"
)

plt.title("T30 vs B30")

plt.savefig(
    "reports/charts/t30_b30.png"
)

plt.close()

# ==================================================
# 10. SECTOR ALLOCATION
# ==================================================

print("Creating sector allocation chart...")

sector_data = (
    holdings
    .groupby("sector")["weight_pct"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 8))

plt.pie(
    sector_data,
    labels=sector_data.index
)

plt.title(
    "Sector Allocation"
)

plt.savefig(
    "reports/charts/sector_allocation.png"
)

plt.close()

# ==================================================
# 11. EXPENSE RATIO DISTRIBUTION
# ==================================================

print("Creating expense ratio chart...")

plt.figure(figsize=(8, 5))

sns.histplot(
    performance["expense_ratio_pct"],
    bins=10
)

plt.title(
    "Expense Ratio Distribution"
)

plt.savefig(
    "reports/charts/expense_ratio_distribution.png"
)

plt.close()

print("All charts created successfully!")

returns = nav.pivot(index="date", columns="amfi_code", values="nav")
returns = returns.pct_change().dropna()

corr = returns.iloc[:, :10].corr()

plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True)
plt.title("NAV Return Correlation Matrix")
plt.savefig("reports/charts/nav_correlation.png")
plt.close()

plt.figure(figsize=(8,5))

transactions["transaction_type"].value_counts().plot(kind="bar")

plt.title("Transaction Types")
plt.savefig("reports/charts/transaction_types.png")
plt.close()

transactions["kyc_status"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")
plt.title("KYC Status")
plt.savefig("reports/charts/kyc_status.png")
plt.close()

performance["fund_house"].value_counts().plot(
    kind="barh",
    figsize=(8,6)
)

plt.title("Fund House Distribution")
plt.savefig("reports/charts/fund_house_distribution.png")
plt.close()

plt.figure(figsize=(10,6))

sns.boxplot(
    x="category",
    y="expense_ratio_pct",
    data=performance
)

plt.xticks(rotation=45)

plt.savefig(
    "reports/charts/expense_by_category.png"
)

plt.close()

