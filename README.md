# Mutual Fund Analytics Capstone Project

## Overview

This project was developed as part of the Bluestock Fintech Internship Capstone Project.

The objective is to build a complete Mutual Fund Analytics platform using Python, SQL, Data Analysis, and Visualization techniques. The project covers data cleaning, ETL pipelines, exploratory data analysis, performance analytics, and dashboard development.

---

## Project Objectives

* Clean and validate mutual fund datasets
* Build a structured SQLite database
* Perform exploratory data analysis (EDA)
* Calculate fund performance metrics
* Compare funds against benchmark indices
* Generate visual analytics and reports
* Build an interactive dashboard
* Develop advanced analytics and portfolio insights

---

## Technology Stack

### Programming Language

* Python 3.11

### Libraries

* Pandas
* NumPy
* Matplotlib
* Seaborn
* SciPy
* SQLAlchemy
* SQLite

### Tools

* VS Code
* PowerShell
* Git
* GitHub
* Jupyter Notebook

---

## Project Structure

```text
fintech_project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── EDA_Analysis.ipynb
│   └── Performance_Analytics.ipynb
│
├── reports/
│   ├── charts/
│   ├── data_dictionary.md
│   └── data_quality_summary.txt
│
├── scripts/
│   ├── clean_nav_history.py
│   ├── clean_transactions.py
│   ├── clean_performance.py
│   ├── load_sqlite.py
│   ├── day3_eda.py
│   ├── day4_performance.py
│   └── bonus/
│       └── scheduler.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
└── README.md
```

---

## Datasets Used

### Processed Files

* 01_fund_master_clean.csv
* 02_nav_history_clean.csv
* 03_aum_by_fund_house_clean.csv
* 04_monthly_sip_inflows_clean.csv
* 05_category_inflows_clean.csv
* 06_industry_folio_count_clean.csv
* 07_scheme_performance_clean.csv
* 08_investor_transactions_clean.csv
* 09_portfolio_holdings_clean.csv
* 10_benchmark_indices_clean.csv

---

## Day 2 Deliverables

### Data Cleaning

Completed cleaning and validation for:

* NAV History
* Investor Transactions
* Scheme Performance

### Database

Created SQLite database and schema.

Generated:

* schema.sql
* queries.sql
* bluestock_mf.db

### Documentation

Created:

* data_dictionary.md
* data_quality_summary.txt

---

## Day 3 Deliverables

### Exploratory Data Analysis

Generated visualizations including:

* NAV Trends
* AUM Growth
* SIP Trend
* Category Heatmap
* Gender Distribution
* Age Distribution
* State-wise Transactions
* Folio Growth
* Sector Allocation
* NAV Correlation Matrix
* Expense Ratio Analysis

### Outputs

* 15+ charts exported as PNG files
* EDA_Analysis.ipynb
* EDA Findings Documentation

---

## Day 4 Deliverables

### Performance Analytics

Calculated:

* Daily Returns
* CAGR
* Sharpe Ratio
* Sortino Ratio
* Alpha
* Beta
* Maximum Drawdown
* Fund Scorecard

### Generated Files

* daily_returns.csv
* cagr.csv
* sharpe_ratio.csv
* sortino_ratio.csv
* alpha_beta.csv
* max_drawdown.csv
* fund_scorecard.csv

### Visualizations

* Benchmark Comparison Chart

### Notebook

* Performance_Analytics.ipynb

---

## Key Performance Metrics

### CAGR

Measures annualized growth rate.

### Sharpe Ratio

Measures risk-adjusted returns.

### Sortino Ratio

Measures downside-risk-adjusted returns.

### Alpha

Measures excess return over benchmark.

### Beta

Measures sensitivity to benchmark movement.

### Maximum Drawdown

Measures largest decline from peak value.

---

## Day 5 Progress – Dashboard Development

### Completed
- Imported cleaned datasets into Power BI
- Established data relationships
- Built Industry Overview dashboard
- Added KPI cards:
  - Total Industry AUM
  - Latest SIP Inflow
  - Total Folios
  - Number of Schemes
- Created Industry AUM Growth visualization
- Created AUM by Fund House comparison chart
- Built Fund Performance & Risk page
- Added Risk vs Return scatter plot
- Added Fund Performance Scorecard
- Added NAV Trend analysis chart
- Added slicers for Fund House, Category and Plan

## Power BI Dashboard

### Dashboard Pages

- Industry Overview
- Fund Performance Analysis
- Investor Analytics
- SIP & Market Trends
- NAV Detail Drill-through Page

### Key Features

- Interactive Power BI dashboard
- Risk vs Return Analysis
- NAV Trend Tracking
- Investor Demographic Analysis
- SIP Growth Monitoring
- Category-wise Inflow Analysis
- Drill-through Navigation
- Bluestock Themed Visuals

### Dashboard Screenshots

#### Industry Overview

![Industry Overview](reports/dashboard/industry_overview.png)

#### Fund Performance

![Fund Performance](reports/dashboard/fund_performance.png)

#### Investor Analytics

![Investor Analytics](reports/dashboard/investor_analysis.png)

#### SIP & Market Trends

![SIP Trends](reports/dashboard/sip_market_trends.png)

## Day 6 - Advanced Analytics + Risk Metrics

Completed advanced mutual fund analytics including:

- Historical VaR at 95%
- CVaR / Expected Shortfall
- Rolling 90-day Sharpe Ratio
- Investor cohort analysis
- SIP continuity risk flagging
- Rule-based fund recommender
- Sector HHI concentration analysis

Generated deliverables:

- notebooks/Advanced_Analytics.ipynb
- data/processed/var_cvar_report.csv
- data/processed/investor_cohort_analysis.csv
- data/processed/sip_continuity_report.csv
- data/processed/fund_recommendations.csv
- data/processed/sector_hhi_report.csv
- scripts/recommender.py
- reports/charts/rolling_sharpe_chart.png

## Bonus Work

## Bonus Challenge B1 – Automated NAV Scheduler

A scheduled ETL process was created to automatically refresh mutual fund NAV data.

Features:
- Runs Monday to Friday
- Scheduled execution at 8:00 PM
- Automatically triggers NAV data refresh
- Uses Python scheduling framework

Files:
- scripts/bonus/scheduler.py
- scripts/bonus/live_nav_fetch.py

Run locally:

py scripts/bonus/scheduler.py
## Bonus Challenge B2 – Streamlit Dashboard

A fully interactive web application was developed using Streamlit as an alternative to Power BI.

Features:
- Industry Overview
- Fund Performance Analytics
- NAV Trend Explorer
- Investor Analytics
- SIP Market Trends
- Fund Recommender

Run locally:

py -m streamlit run dashboard/streamlit/app.py

## Bonus Challenge B3 – Mutual Fund Return Prediction

A machine learning-based mutual fund return prediction model was developed using Random Forest Regression.

Features:
- Predicts 3-Year Mutual Fund Returns
- Uses Fund Performance Metrics as Input Features
- Feature Importance Analysis
- Model Evaluation using MAE, RMSE, and R² Score
- Exported Trained Model for Future Predictions
- Generated Prediction Output Dataset

Input Features:
- Expense Ratio
- Sharpe Ratio
- Sortino Ratio
- Alpha
- Beta
- Annualized Standard Deviation
- Maximum Drawdown

Model Performance:
- MAE: 1.07
- RMSE: 1.55
- R² Score: 0.9058

Key Finding:
- Annualized Volatility (Standard Deviation) was the most influential factor affecting long-term mutual fund returns.

Outputs:
- models/fund_return_predictor.pkl
- reports/charts/fund_feature_importance.png
- data/processed/fund_feature_importance.csv
- data/processed/fund_return_predictions.csv

Run locally:

py .\ml\fund_predictor.py

## Bonus Challenge B4 – Monte Carlo NAV Simulation

A Monte Carlo simulation model was created to project possible future NAV paths for a selected mutual fund over a 5-year horizon.

Features:
- Uses historical daily NAV returns
- Simulates 1,000 possible future NAV paths
- Projects NAV movement over 5 trading years
- Calculates mean projection, 5th percentile, and 95th percentile bands
- Generates uncertainty-based NAV forecast chart

Outputs:
- data/processed/monte_carlo_results.csv
- reports/charts/monte_carlo_simulation.png

Run locally:

py .\ml\monte_carlo_simulation.py


## Git Workflow

```bash
git add .
git commit -m "Project update"
git push
```

---

## Author

Anushka Das

Bluestock Fintech Internship

Capstone Project I – Mutual Fund Analytics
