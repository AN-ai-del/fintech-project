from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "07_scheme_performance_clean.csv"
MODEL_DIR = BASE_DIR / "models"
CHART_DIR = BASE_DIR / "reports" / "charts"

MODEL_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

print("Loading scheme performance dataset...")

df = pd.read_csv(DATA_PATH)

features = [
    "expense_ratio_pct",
    "sharpe_ratio",
    "sortino_ratio",
    "alpha",
    "beta",
    "std_dev_ann_pct",
    "max_drawdown_pct"
]

target = "return_3yr_pct"

X = df[features].copy()
y = df[target].copy()

X = X.fillna(X.mean())
y = y.fillna(y.mean())

print("Training Random Forest model...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANCE")
print("------------------")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R2   : {r2:.4f}")

importance = pd.DataFrame(
    {
        "feature": features,
        "importance": model.feature_importances_
    }
)

importance = importance.sort_values(
    "importance",
    ascending=False
)

importance.to_csv(
    BASE_DIR / "data" / "processed" / "fund_feature_importance.csv",
    index=False
)

print("\nFEATURE IMPORTANCE")
print("------------------")
print(importance)

plt.figure(figsize=(9, 5))
plt.barh(
    importance["feature"],
    importance["importance"]
)
plt.gca().invert_yaxis()
plt.title("Feature Importance for 3-Year Return Prediction")
plt.xlabel("Importance")
plt.tight_layout()

chart_path = CHART_DIR / "fund_feature_importance.png"
plt.savefig(chart_path)
plt.close()

model_path = MODEL_DIR / "fund_return_predictor.pkl"
joblib.dump(model, model_path)

predictions_df = pd.DataFrame(
    {
        "actual_return_3yr_pct": y_test.values,
        "predicted_return_3yr_pct": predictions
    }
)

predictions_df.to_csv(
    BASE_DIR / "data" / "processed" / "fund_return_predictions.csv",
    index=False
)

print("\nSaved files:")
print(model_path)
print(chart_path)
print(BASE_DIR / "data" / "processed" / "fund_feature_importance.csv")
print(BASE_DIR / "data" / "processed" / "fund_return_predictions.csv")