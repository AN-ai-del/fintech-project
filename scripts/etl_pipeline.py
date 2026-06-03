import subprocess
import sys

print("=" * 60)
print("BLUESTOCK MUTUAL FUND ETL PIPELINE")
print("=" * 60)

scripts = [
    "scripts/data_ingestion.py",
    "scripts/live_nav_fetch.py",
    "scripts/validate_amfi.py",
    "scripts/clean_nav_history.py",
    "scripts/clean_transactions.py",
    "scripts/clean_performance.py",
    "scripts/load_sqlite.py"
]

for script in scripts:
    print(f"\nRunning {script}")

    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("ERROR:")
        print(result.stderr)
        break

print("\nETL Pipeline Completed")

print("\n" + "="*50)
print("DATA VALIDATION SUMMARY")
print("="*50)

print(f"Fund Master Rows: {len(pd.read_csv('data/processed/01_fund_master_clean.csv'))}")
print(f"NAV History Rows: {len(pd.read_csv('data/processed/02_nav_history_clean.csv'))}")
print(f"Transactions Rows: {len(pd.read_csv('data/processed/08_investor_transactions_clean.csv'))}")

print("\nETL PIPELINE SUCCESSFULLY COMPLETED")