-- 1. Top 5 funds by AUM
SELECT
    scheme_name,
    aum_crore
FROM performance
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV by Month
SELECT
    substr(date,1,7) AS month,
    AVG(nav) AS avg_nav
FROM nav_history
GROUP BY month
ORDER BY month;

-- 3. Average 1-Year Return by Category
SELECT
    category,
    AVG(return_1yr_pct) AS avg_return
FROM performance
GROUP BY category
ORDER BY avg_return DESC;

-- 4. Funds with Expense Ratio Below 1%
SELECT
    scheme_name,
    expense_ratio_pct
FROM performance
WHERE expense_ratio_pct < 1;

-- 5. Total Transactions by State
SELECT
    state,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY state
ORDER BY transaction_count DESC;

-- 6. Total Investment Amount by State
SELECT
    state,
    SUM(amount_inr) AS total_amount
FROM transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 7. Average Transaction Amount by Transaction Type
SELECT
    transaction_type,
    AVG(amount_inr) AS avg_amount
FROM transactions
GROUP BY transaction_type;

-- 8. Top 10 Funds by 5-Year Return
SELECT
    scheme_name,
    return_5yr_pct
FROM performance
ORDER BY return_5yr_pct DESC
LIMIT 10;

-- 9. Fund Count by Category
SELECT
    category,
    COUNT(*) AS fund_count
FROM fund_master
GROUP BY category
ORDER BY fund_count DESC;

-- 10. Average Expense Ratio by Fund House
SELECT
    fund_house,
    AVG(expense_ratio_pct) AS avg_expense_ratio
FROM performance
GROUP BY fund_house
ORDER BY avg_expense_ratio;