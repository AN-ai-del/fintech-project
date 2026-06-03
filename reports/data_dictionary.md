# Mutual Fund Analytics - Data Dictionary

## Dataset 1: Fund Master

Source: 01_fund_master.csv

| Column             | Data Type | Description                   |
| ------------------ | --------- | ----------------------------- |
| amfi_code          | Integer   | Unique AMFI scheme identifier |
| fund_house         | String    | Asset Management Company      |
| scheme_name        | String    | Mutual fund scheme name       |
| category           | String    | Fund category                 |
| sub_category       | String    | Fund sub-category             |
| plan               | String    | Direct or Regular plan        |
| launch_date        | Date      | Scheme launch date            |
| benchmark          | String    | Benchmark index               |
| expense_ratio_pct  | Float     | Expense ratio percentage      |
| exit_load_pct      | Float     | Exit load percentage          |
| min_sip_amount     | Integer   | Minimum SIP amount            |
| min_lumpsum_amount | Integer   | Minimum lump sum investment   |
| fund_manager       | String    | Fund manager name             |
| risk_category      | String    | Risk classification           |
| sebi_category_code | String    | SEBI category code            |

## Dataset 2: NAV History

Source: 02_nav_history.csv

| Column    | Data Type | Description       |
| --------- | --------- | ----------------- |
| amfi_code | Integer   | Scheme identifier |
| date      | Date      | NAV date          |
| nav       | Float     | Net Asset Value   |

## Dataset 3: AUM by Fund House

Source: 03_aum_by_fund_house.csv

| Column         | Data Type | Description              |
| -------------- | --------- | ------------------------ |
| date           | Date      | Reporting date           |
| fund_house     | String    | Asset management company |
| aum_lakh_crore | Float     | AUM in lakh crore        |
| aum_crore      | Integer   | AUM in crore             |
| num_schemes    | Integer   | Number of schemes        |

## Dataset 4: Monthly SIP Inflows

Source: 04_monthly_sip_inflows.csv

| Column                    | Data Type | Description                      |
| ------------------------- | --------- | -------------------------------- |
| month                     | String    | Month                            |
| sip_inflow_crore          | Integer   | SIP inflow amount                |
| active_sip_accounts_crore | Float     | Active SIP accounts              |
| new_sip_accounts_lakh     | Float     | Newly registered SIP accounts    |
| sip_aum_lakh_crore        | Float     | SIP AUM                          |
| yoy_growth_pct            | Float     | Year-over-year growth percentage |

## Dataset 5: Category Inflows

Source: 05_category_inflows.csv

Contains monthly net inflows across mutual fund categories.

## Dataset 6: Industry Folio Count

Source: 06_industry_folio_count.csv

Contains folio counts by segment.

## Dataset 7: Scheme Performance

Source: 07_scheme_performance.csv

Contains returns, risk metrics, ratings, and performance indicators.

## Dataset 8: Investor Transactions

Source: 08_investor_transactions.csv

Contains investor transaction records including SIPs, redemptions, and lump sum investments.

## Dataset 9: Portfolio Holdings

Source: 09_portfolio_holdings.csv

Contains stock holdings and portfolio allocations.

## Dataset 10: Benchmark Indices

Source: 10_benchmark_indices.csv

Contains historical benchmark index values.
