# FP&A Actuals_vs_budget Variance Analysis and Forecast

## What this is
A variance analysis comparing actual sales performance against a constructed
budget (prior-year actuals grown 8% YoY, a standard top-down FP&A technique
used when no bottom-up budget exists), plus a 3-month forward forecast.

## Data source
"Superstore Dataset" — Kaggle (vivek468)

## Methodology note
No public dataset contains real internal budgets. This project constructs a
defensible budget baseline using a standard top-down FP&A technique: prior-year
same-month actuals grown by a target rate.

**Revision:** the initial version applied a single flat 8% growth rate across
all categories. Testing that assumption against each category's actual
historical YoY growth (Furniture: 8.5% median, Office Supplies: 33.8%,
Technology: 20.0%) showed a flat rate was misrepresenting category-specific
volatility — particularly for Technology, whose swings (-71% to +364% variance
in the original version) were partly an artifact of forcing one growth
assumption onto its most volatile category.

The model now uses **moderated, category-specific growth targets** rather
than the raw historical medians directly, since the historical figures are
based on a limited number of yearly periods and directly adopting them would
overfit to a small, noisy sample:

| Category | Historical Median YoY Growth | Growth Target Used |
| Furniture | 8.5% | 8% |
| Office Supplies | 33.8% | 15% |
| Technology | 20.0% | 10% |

This is a real limitation worth stating plainly: even category-specific
targets are still a simplification, and don't account for one-off anomalies,
promotions, or genuine market shifts within a given year. A more rigorous
version would apply outlier detection to the base-year actuals before
computing growth, and use a budget *range* rather than a single point estimate.

## Tools
Excel (inspection, FORECAST.LINEAR validation) → Python/pandas + scikit-learn
(budget construction, forecasting) → MySQL (variance analysis) → Power BI (dashboard)

## Key findings
- Overall: the business modestly beat budget — $1.8M actual vs. $1.7M budget, a total variance of +$123.8K (~7% over plan).
- Sales by category is well-balanced, not concentrated: Technology contributes 36.45%, Office Supplies 31.3%, while Furniture has 32.26% of actual sales. So, no single category is carrying or dragging the business.
- Technology is the most volatile category so far. It shows up multiple times in the 5 best performing periods table as well as the 5 worst performing periods table, in fact occupying 4/5 slots in the latter. Combined with the Max Variance (335.55%) and Min Variance (-72.86%) KPI cards, this tells that sales of Technology products fluctuate harder in both directions than the other categories.
- A clear improvement trend over time is visible through both the aforementioned tables and the actuals_vs_budget line chart. The worst-performing periods cluster almost entirely in 2015 (March, July, September), while the best-performing periods cluster in 2016–2017. Even the yearly variance waterfall confirms this directly — 2015, in the red column, shows that aggregate sales was under budget, then 2016 and 2017 both were meaningfully over budget.
- The 3-month forecast is trending downward — the red-dashed forecast line in the line chart slightly dips at the end. Given 2015 was the only underperforming year, a projected downturn is worth flagging before it becomes a repeat pattern.

## Recommendations / Business Implications
- Put a variance investigation threshold (e.g., ±20% in a single month triggering a root-cause review). Right now on this dashboard, fluctuations up to +271% and down to -71% are visible only in hindsight. If a threshold variance is implemented, instead of simply reporting the fluctuations later, we can use it as an early-warning tool and improve sales by investing the underlying driving factors.
- Investigate what's actually driving Technology's sales fluctuations. Perhaps it's the product launch timing, promotional discounting, or seasonal demand (e.g. holiday electronics). Once identified, that driver should determine next year's category-level budget rather than just a blanket growth rate.
- The downward 3-month forecast should be treated as an early signal. Investigating the cause immediately can prevent a later loss.

## Dashboard
[Dashboard](screenshots/Dashboard.png)

## Files
- `notebooks/FP&A_analysis_forecast.py` — budget construction, forecasting
- `excel/Sample - Superstore_transformed.csv` — cleaned dataset
- `excel/budget_vs_actuals.csv` — budget_vs_actuals table
- `excel/Forecast_Sales.csv` — Forecast table
- `sql/fpa_analysis_queries.sql` — analysis queries
- `excel/sql query results_and pivot table_forecast.xlxs` — queries outputs and pivot table combined
- `dashboard/FP&A Variance and Forecast Dashboard.pdf` — Power BI file
