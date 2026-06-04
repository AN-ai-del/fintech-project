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

## Bonus Work

### Automated Scheduler

Implemented a scheduler script for future automation tasks.

File:

```text
scripts/bonus/scheduler.py
```

Future enhancements:

* Automated NAV fetching
* Scheduled ETL execution
* Report generation

---

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
