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