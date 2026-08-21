CREATE DATABASE fpa_analysis;
USE fpa_analysis;
DESCRIBE budget_vs_actuals;

SELECT * FROM budget_vs_actuals;

SELECT Category,
ROUND(SUM(Actual_Sales),0) AS Total_actual,
ROUND(SUM(Budget_Sales), 0) AS Total_budget,
ROUND(SUM(Variance_Sales), 0) AS Total_Variance,
ROUND((SUM(Variance_Sales)/SUM(Budget_Sales))*100, 1) AS variance_pct
FROM budget_vs_actuals
GROUP BY Category
ORDER BY Variance_pct DESC;

SELECT YearMonth,
ROUND(SUM(Actual_Sales),0) AS Total_actual,
ROUND(SUM(Budget_Sales), 0) AS Total_budget,
ROUND(SUM(Variance_Sales), 0) AS Total_Variance
FROM budget_vs_actuals
GROUP BY YearMonth
ORDER BY YearMonth;

SELECT YearMonth, Category, ROUND(Actual_Sales, 1) AS Actual_Sales, 
ROUND(Budget_Sales, 1) AS Budget_Sales, 
ROUND(Variance_Sales, 1) AS Variance_Sales, Variance_pct
FROM budget_vs_actuals
ORDER BY Variance_pct ASC
LIMIT 10;

SELECT YearMonth, Category, ROUND(Actual_Sales, 1) AS Actual_Sales, 
ROUND(Budget_Sales, 1) AS Budget_Sales, 
ROUND(Variance_Sales, 1) AS Variance_Sales, Variance_pct
FROM budget_vs_actuals
ORDER BY Variance_pct DESC
LIMIT 10;

SELECT YearMonth, Category, ROUND(Variance_Sales, 1) AS Variance_Sales,
ROUND(SUM(Variance_Sales) OVER(PARTITION BY Category, LEFT(YearMonth, 4)
ORDER BY YearMonth), 1) AS Cumulative_variance
FROM budget_vs_actuals
ORDER BY Category, YearMonth;

