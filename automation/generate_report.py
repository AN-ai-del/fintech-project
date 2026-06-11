from pathlib import Path
import pandas as pd
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

print("Loading datasets...")

aum = pd.read_csv(DATA_DIR / "03_aum_by_fund_house_clean.csv")
sip = pd.read_csv(DATA_DIR / "04_monthly_sip_inflows_clean.csv")
folios = pd.read_csv(DATA_DIR / "06_industry_folio_count_clean.csv")
performance = pd.read_csv(DATA_DIR / "07_scheme_performance_clean.csv")
var_cvar = pd.read_csv(DATA_DIR / "var_cvar_report.csv")
recommendations = pd.read_csv(DATA_DIR / "fund_recommendations.csv")
monte_carlo = pd.read_csv(DATA_DIR / "monte_carlo_results.csv")
efficient_frontier = pd.read_csv(DATA_DIR / "efficient_frontier_results.csv")

latest_aum = aum["aum_lakh_crore"].max()
latest_sip = sip["sip_inflow_crore"].max()
latest_folios = folios["total_folios_crore"].max()

top_sharpe = (
    performance.sort_values("sharpe_ratio", ascending=False)
    .head(5)[["scheme_name", "fund_house", "category", "return_3yr_pct", "sharpe_ratio"]]
)

highest_risk = (
    var_cvar.sort_values("var_95")
    .head(5)[["scheme_name", "fund_house", "category", "var_95", "cvar_95"]]
)

best_portfolio = efficient_frontier.loc[
    efficient_frontier["sharpe"].idxmax()
]

final_monte_carlo = monte_carlo.iloc[-1]

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bluestock Weekly Mutual Fund Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 90%;
            margin: auto;
            padding: 30px;
        }}
        .header {{
            background-color: #1e40af;
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 25px;
        }}
        .header h1 {{
            margin: 0;
        }}
        .cards {{
            display: flex;
            gap: 20px;
            margin-bottom: 25px;
        }}
        .card {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            flex: 1;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .card h2 {{
            margin: 0;
            color: #2563eb;
            font-size: 28px;
        }}
        .section {{
            background-color: white;
            padding: 22px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th {{
            background-color: #1e40af;
            color: white;
            padding: 10px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .footer {{
            text-align: center;
            color: #64748b;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">

        <div class="header">
            <h1>Bluestock Weekly Mutual Fund Performance Report</h1>
            <p>Generated on {datetime.now().strftime("%d %B %Y, %I:%M %p")}</p>
        </div>

        <div class="cards">
            <div class="card">
                <p>Total Industry AUM</p>
                <h2>{latest_aum:.2f} L Cr</h2>
            </div>
            <div class="card">
                <p>Peak SIP Inflow</p>
                <h2>₹{latest_sip:,.0f} Cr</h2>
            </div>
            <div class="card">
                <p>Total Folios</p>
                <h2>{latest_folios:.2f} Cr</h2>
            </div>
        </div>

        <div class="section">
            <h2>Top 5 Funds by Sharpe Ratio</h2>
            {top_sharpe.to_html(index=False)}
        </div>

        <div class="section">
            <h2>Highest Downside Risk Funds by VaR</h2>
            {highest_risk.to_html(index=False)}
        </div>

        <div class="section">
            <h2>Monte Carlo Forecast Summary</h2>
            <p>The 5-year Monte Carlo projection produced the following final NAV estimates:</p>
            <ul>
                <li><b>Mean projected NAV:</b> {final_monte_carlo["mean_nav"]:.2f}</li>
                <li><b>5th percentile NAV:</b> {final_monte_carlo["p5_nav"]:.2f}</li>
                <li><b>95th percentile NAV:</b> {final_monte_carlo["p95_nav"]:.2f}</li>
            </ul>
        </div>

        <div class="section">
            <h2>Efficient Frontier Summary</h2>
            <p>The best simulated portfolio based on Sharpe Ratio had:</p>
            <ul>
                <li><b>Expected Return:</b> {best_portfolio["return"]:.2%}</li>
                <li><b>Risk / Volatility:</b> {best_portfolio["risk"]:.2%}</li>
                <li><b>Sharpe Ratio:</b> {best_portfolio["sharpe"]:.2f}</li>
            </ul>
        </div>

        <div class="section">
            <h2>Fund Recommendations Snapshot</h2>
            {recommendations.head(9).to_html(index=False)}
        </div>

        <div class="footer">
            <p>Generated automatically using Python, Pandas and HTML.</p>
            <p>Bluestock Mutual Fund Analytics Capstone Project</p>
        </div>

    </div>
</body>
</html>
"""

output_path = REPORTS_DIR / "weekly_performance_report.html"

with open(output_path, "w", encoding="utf-8") as file:
    file.write(html)

print("HTML report generated successfully.")
print(output_path)