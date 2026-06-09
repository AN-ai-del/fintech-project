from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"

performance = pd.read_csv(DATA_DIR / "07_scheme_performance_clean.csv")

if "risk_grade" in performance.columns:
    risk_col = "risk_grade"
else:
    risk_col = "risk_category"


def recommend_funds(risk_appetite):
    risk_appetite = risk_appetite.strip().lower()

    matched = performance[
        performance[risk_col].str.lower() == risk_appetite
    ].copy()

    if matched.empty:
        print("No funds found for this risk appetite.")
        print("Try: Low, Moderate, High, or Very High")
        return

    matched = matched.sort_values(
        "sharpe_ratio",
        ascending=False
    )

    recommendations = matched[
        [
            "amfi_code",
            "scheme_name",
            "fund_house",
            "category",
            "return_3yr_pct",
            "sharpe_ratio",
            risk_col
        ]
    ].head(3)

    print("\nTop 3 Recommended Funds\n")
    print(recommendations.to_string(index=False))


if __name__ == "__main__":
    print("Mutual Fund Recommender")
    print("Risk options: Low, Moderate, High, Very High")

    user_risk = input("Enter your risk appetite: ")

    recommend_funds(user_risk)