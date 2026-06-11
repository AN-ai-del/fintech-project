from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"

st.set_page_config(
    page_title="Bluestock Mutual Fund Analytics",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    fund_master = pd.read_csv(DATA_DIR / "01_fund_master_clean.csv")
    nav = pd.read_csv(DATA_DIR / "02_nav_history_clean.csv")
    aum = pd.read_csv(DATA_DIR / "03_aum_by_fund_house_clean.csv")
    sip = pd.read_csv(DATA_DIR / "04_monthly_sip_inflows_clean.csv")
    category = pd.read_csv(DATA_DIR / "05_category_inflows_clean.csv")
    folios = pd.read_csv(DATA_DIR / "06_industry_folio_count_clean.csv")
    performance = pd.read_csv(DATA_DIR / "07_scheme_performance_clean.csv")
    transactions = pd.read_csv(DATA_DIR / "08_investor_transactions_clean.csv")
    return fund_master, nav, aum, sip, category, folios, performance, transactions

fund_master, nav, aum, sip, category, folios, performance, transactions = load_data()

nav["date"] = pd.to_datetime(nav["date"])
aum["date"] = pd.to_datetime(aum["date"])
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])

st.title("📊 Bluestock Mutual Fund Analytics Platform")
st.caption("Bonus Challenge B2 — Streamlit Web App Alternative to Power BI")

page = st.sidebar.radio(
    "Select Dashboard Page",
    [
        "Industry Overview",
        "Fund Performance",
        "Investor Analytics",
        "SIP & Market Trends",
        "Fund Recommender"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("Built using Python, Pandas and Streamlit")

if page == "Industry Overview":
    st.header("Industry Overview")

    latest_aum = aum["aum_lakh_crore"].max()
    latest_sip = sip["sip_inflow_crore"].max()
    latest_folios = folios["total_folios_crore"].max()
    schemes = aum["num_schemes"].max()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Industry AUM", f"{latest_aum:.2f} L Cr")
    col2.metric("Peak SIP Inflow", f"₹{latest_sip:,.0f} Cr")
    col3.metric("Total Folios", f"{latest_folios:.2f} Cr")
    col4.metric("Number of Schemes", f"{schemes:,.0f}")

    st.subheader("AUM Trend")
    aum_trend = (
        aum.groupby("date")["aum_lakh_crore"]
        .sum()
        .reset_index()
        .set_index("date")
    )
    st.line_chart(aum_trend)

    st.subheader("AUM by Fund House")
    aum_by_house = (
        aum.groupby("fund_house")["aum_lakh_crore"]
        .max()
        .sort_values(ascending=False)
    )
    st.bar_chart(aum_by_house)

elif page == "Fund Performance":
    st.header("Fund Performance & Risk")

    fund_house_options = ["All"] + sorted(performance["fund_house"].dropna().unique().tolist())
    category_options = ["All"] + sorted(performance["category"].dropna().unique().tolist())

    col1, col2 = st.columns(2)

    selected_fund_house = col1.selectbox("Fund House", fund_house_options)
    selected_category = col2.selectbox("Category", category_options)

    filtered_perf = performance.copy()

    if selected_fund_house != "All":
        filtered_perf = filtered_perf[filtered_perf["fund_house"] == selected_fund_house]

    if selected_category != "All":
        filtered_perf = filtered_perf[filtered_perf["category"] == selected_category]

    st.subheader("Risk vs Return Data")
    st.scatter_chart(
        filtered_perf,
        x="return_3yr_pct",
        y="std_dev_ann_pct",
        size="aum_crore"
    )

    st.subheader("Top Funds by Sharpe Ratio")
    st.dataframe(
        filtered_perf[
            [
                "scheme_name",
                "fund_house",
                "category",
                "return_3yr_pct",
                "sharpe_ratio",
                "sortino_ratio",
                "alpha",
                "beta",
                "expense_ratio_pct"
            ]
        ].sort_values("sharpe_ratio", ascending=False),
        use_container_width=True
    )

    st.subheader("NAV Trend for Selected Fund")

    selected_scheme = st.selectbox(
        "Select Scheme",
        performance["scheme_name"].dropna().unique()
    )

    selected_code = performance.loc[
        performance["scheme_name"] == selected_scheme,
        "amfi_code"
    ].iloc[0]

    selected_nav = nav[nav["amfi_code"] == selected_code].copy()
    selected_nav = selected_nav.set_index("date")[["nav"]]

    st.line_chart(selected_nav)

elif page == "Investor Analytics":
    st.header("Investor Analytics")

    state_options = ["All"] + sorted(transactions["state"].dropna().unique().tolist())
    age_options = ["All"] + sorted(transactions["age_group"].dropna().unique().tolist())
    city_options = ["All"] + sorted(transactions["city_tier"].dropna().unique().tolist())

    col1, col2, col3 = st.columns(3)

    selected_state = col1.selectbox("State", state_options)
    selected_age = col2.selectbox("Age Group", age_options)
    selected_city = col3.selectbox("City Tier", city_options)

    filtered_txn = transactions.copy()

    if selected_state != "All":
        filtered_txn = filtered_txn[filtered_txn["state"] == selected_state]

    if selected_age != "All":
        filtered_txn = filtered_txn[filtered_txn["age_group"] == selected_age]

    if selected_city != "All":
        filtered_txn = filtered_txn[filtered_txn["city_tier"] == selected_city]

    st.subheader("Transaction Amount by State")
    state_amount = (
        filtered_txn.groupby("state")["amount_inr"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(state_amount)

    st.subheader("Transaction Type Distribution")
    txn_type = filtered_txn.groupby("transaction_type")["amount_inr"].sum()
    st.bar_chart(txn_type)

    st.subheader("Average Investment by Age Group")
    age_amount = filtered_txn.groupby("age_group")["amount_inr"].mean()
    st.bar_chart(age_amount)

    st.subheader("Gender Distribution")
    gender_count = filtered_txn["gender"].value_counts()
    st.bar_chart(gender_count)

elif page == "SIP & Market Trends":
    st.header("SIP & Market Trends")

    st.subheader("Monthly SIP Inflows")
    sip_trend = sip.set_index("month")[["sip_inflow_crore"]]
    st.line_chart(sip_trend)

    st.subheader("Active SIP Accounts")
    active_sip = sip.set_index("month")[["active_sip_accounts_crore"]]
    st.line_chart(active_sip)

    st.subheader("Category-wise Net Inflows")
    category_inflow = (
        category.groupby("category")["net_inflow_crore"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(category_inflow)

    st.subheader("Top 5 Categories by Net Inflow")
    st.bar_chart(category_inflow.head(5))

elif page == "Fund Recommender":
    st.header("Simple Fund Recommender")

    risk_options = sorted(performance["risk_grade"].dropna().unique().tolist())

    selected_risk = st.selectbox("Select Risk Appetite", risk_options)

    recommendations = (
        performance[performance["risk_grade"] == selected_risk]
        .sort_values("sharpe_ratio", ascending=False)
        .head(3)
    )

    st.subheader("Top 3 Recommended Funds")

    st.dataframe(
        recommendations[
            [
                "scheme_name",
                "fund_house",
                "category",
                "return_3yr_pct",
                "sharpe_ratio",
                "sortino_ratio",
                "expense_ratio_pct",
                "risk_grade"
            ]
        ],
        use_container_width=True
    )