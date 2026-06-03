import pandas as pd

files = [
    ("01_fund_master.csv", "01_fund_master_clean.csv"),
    ("03_aum_by_fund_house.csv", "03_aum_by_fund_house_clean.csv"),
    ("04_monthly_sip_inflows.csv", "04_monthly_sip_inflows_clean.csv"),
    ("05_category_inflows.csv", "05_category_inflows_clean.csv"),
    ("06_industry_folio_count.csv", "06_industry_folio_count_clean.csv"),
    ("09_portfolio_holdings.csv", "09_portfolio_holdings_clean.csv"),
    ("10_benchmark_indices.csv", "10_benchmark_indices_clean.csv")
]

for source, target in files:
    df = pd.read_csv(f"data/raw/{source}")

    df.to_csv(
        f"data/processed/{target}",
        index=False
    )

    print(f"Created {target}")